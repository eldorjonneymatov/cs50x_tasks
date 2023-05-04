import os
import secrets
import asyncio
import configparser
import pandas as pd
import datetime
from telethon import TelegramClient, functions, events, sync, types
from telethon.errors.rpcerrorlist import SendCodeUnavailableError, PhoneCodeInvalidError, FloodWaitError, PhoneNumberInvalidError, AuthKeyUnregisteredError
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import Chat
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import cyrillic_to_latin, drop_channel_sign, apology, login_required, string_to_tuple

# Configure application
app = Flask(__name__)

app.secret_key = secrets.token_hex(16)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///ts.db")

# Reading Configs
config = configparser.ConfigParser()
config.read("config.ini")

# Setting configuration values
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']

api_hash = str(api_hash)
session_name = 'session_name.session'
if not os.path.exists(session_name):
    with open(session_name, mode='w'):
        pass

# Create a new TelegramClient instance with API credentials

client = TelegramClient('session_name', api_id, api_hash)

loop, loop2 = asyncio.get_event_loop(), asyncio.get_event_loop()

CHATS = []
HASH, BEGIN = None, None

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    global CHATS
    chats = db.execute("SELECT username FROM channels WHERE channel_id in (SELECT channel_id FROM followings WHERE user_id = ?)", session["user_id"])
    if not chats:
        return apology("You don`t have any channels")
    CHATS = [chat['username'] for chat in chats]
    try:
        titles = loop.run_until_complete(get_channels_titles())
    except AuthKeyUnregisteredError:
        return apology("There is a problem with your telegram account")
    BEGIN = session.get('last_time')
    if not BEGIN:
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        BEGIN = yesterday.strftime("(%Y, %m, %d, %H, %M, %S)")
        session['last_time'] = BEGIN
    return render_template("/index.html", channels = titles)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        global HASH
        phone = request.form.get("phone")
        rows = db.execute("SELECT * FROM users WHERE phone = ?", phone)
        if not phone or rows:
            return apology("Phone is not available")

        password = request.form.get("password")
        if not password:
            return apology("missing password")

        confirmation = request.form.get("confirmation")
        if password != confirmation:
            return apology("passwords don`t match")

        session['phone'] = phone
        HASH = generate_password_hash(password)

        return send_verification()
    else:
        return render_template('/register.html')


@app.route("/send_verification", methods=["POST"])
def send_verification():
    try:
        loop.run_until_complete(send_code_request())
    except (PhoneNumberInvalidError, TypeError):
        loop.run_until_complete(disconnect_client())
        return apology('Invalid phone number', 401)
    except SendCodeUnavailableError as e:
        loop.run_until_complete(disconnect_client())
        return apology('Verification code unavailable', 401)
    except FloodWaitError as e:
        loop.run_until_complete(disconnect_client())
        return apology(f'Too many requests, please wait {e.seconds} seconds')
    return render_template("/confirm.html")


@app.route("/confirm", methods=["POST", "GET"])
def confirm():
    if request.method == "POST":
        global CHATS
        code = request.form.get("confirm")
        if not code:
            return apology("missing verification code")
        try:
            loop.run_until_complete(sign_in(session['phone'], code))
        except PhoneCodeInvalidError as e:
            loop.run_until_complete(disconnect_client())
            return apology("invalid validation code")
        db.execute("INSERT INTO users (phone, hash) VALUES(?, ?)", session['phone'], HASH)
        user_id = db.execute("SELECT id FROM users WHERE phone = ?", session['phone'])[0]['id']
        try:
            CHATS = loop.run_until_complete(get_public_channels())
        except AuthKeyUnregisteredError:
            return apology('There is a problem with your telegram account')
        for chat in CHATS:
            id = db.execute("SELECT channel_id FROM channels WHERE username = ?", chat)
            if not id:
                if not chat: return apology(CHATS[0])
                db.execute("INSERT INTO channels (username) VALUES(?)", chat)
            id = db.execute("SELECT channel_id FROM channels WHERE username = ?", chat)[0]["channel_id"]
            db.execute("INSERT INTO followings (channel_id, user_id) VALUES(?, ?)", id, user_id)
        return render_template("/registered.html")
    else:
        return render_template("/confirm.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure phone number was submitted
        if not request.form.get("phone"):
            return apology("must provide phone", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for phone
        rows = db.execute("SELECT * FROM users WHERE phone = ?", request.form.get("phone"))

        # Ensure phone exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid phone and/or password", 403)

        user_id = rows[0]['id']
        session['user_id'] = user_id

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("/login.html")


@app.route("/messages", methods=["POST", "GET"])
@login_required
def show_messages():
    if request.method == "POST":
        global DATA
        try:
            loop.run_until_complete(get_messages())
        except AuthKeyUnregisteredError:
            return apology('There is a problem with your telegram account')
        DATA['date'] = pd.to_datetime(DATA['date'])
        messages = DATA[DATA['ad'] == 0]
        ads = DATA[DATA['ad'] == 1]
        messages = messages.sort_values(by='date')
        ads = ads.sort_values(by='date')
        return render_template("/messages.html", messages=messages, ads=ads)
    else:
        return render_template('/')


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


async def send_code_request():
    try:
        await client.connect()
        await client.send_code_request(session['phone'])
    except:
        return


async def sign_in(phone, code):
    await client.sign_in(phone, code)


async def get_public_channels():
    await client.connect()
    channels = []
    async for dialog in client.iter_dialogs():
        if not dialog.is_group and dialog.is_channel:
            channel = await client.get_entity(dialog.id)
            username = channel.username
            if username:
                channels.append(username)
    return channels


async def get_channels_titles():
    global CHATS
    await client.connect()
    titles = []
    async for dialog in client.iter_dialogs():
        if not dialog.is_group and dialog.is_channel:
            channel = await client.get_entity(dialog.id)
            username = channel.username
            if username:
                titles.append({'username': username, 'title': dialog.name})
    return titles


async def get_messages():
    global DATA
    await client.connect()
    DATA = pd.DataFrame({"link":[], "date":[], "text":[], "ad":[]})
    BEGIN = session['last_time']
    BEGIN = string_to_tuple(BEGIN)
    BEGIN = datetime.datetime(*BEGIN)
    # Iterate through channels
    for CHAT in CHATS:
        chat = await client.get_entity(CHAT)
        links, dates, texts, ad = [], [], [], []
        # Iterate through messages in the channel
        async for message in client.iter_messages(chat, reverse=True, offset_date=BEGIN):
            if message.text:
                links.append(f"{CHAT}/{message.id}")
                dates.append(message.date)
                texts.append(cyrillic_to_latin(message.text))
        if texts: texts, ad = drop_channel_sign(texts)
        chat_df = pd.DataFrame({'link': links, 'date': dates, 'text': texts, 'ad': ad})
        DATA = pd.concat([DATA, chat_df])
    current_date_time = datetime.datetime.now()
    BEGIN = current_date_time.strftime("(%Y, %m, %d, %H, %M, %S)")
    # session['last_time'] = BEGIN
    DATA.to_csv(f"{session['user_id']}_data.csv", index=False)