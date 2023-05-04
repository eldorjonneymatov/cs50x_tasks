import os
import secrets
import asyncio
import configparser
import pandas as pd
import datetime
from telethon import TelegramClient, functions, events, sync, types
from telethon.errors.rpcerrorlist import SendCodeUnavailableError, PhoneCodeInvalidError, FloodWaitError, PhoneNumberInvalidError
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import Chat
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import cyrillic_to_latin, drop_channel_sign, apology, login_required

# Configure application
app = Flask(__name__)

app.secret_key = secrets.token_hex(16)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Create a new TelegramClient instance with API credentials

CHATS, CHANNELS = [], {}
HASH = None

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
#     global CHATS
#     chats = db.execute("SELECT username FROM channels WHERE channel_id in (SELECT channel_id FROM followings WHERE user_id = ?)", session["user_id"])
#     CHATS = [chat['username'] for chat in chats]
#     loop.run_until_complete(channel_info())
    CHANNELS = [{'username':'kunonline', 'title':'Kun.uz Tezkor', 'about':'Kun.uz’ning tezkor yangiliklar uchun kanali\nRasmiy kanal (Kirill): @kunuzofficial\nRasmiy kanal (Lotin): @kunuz\nRus tilidagi xabarlar: @kunuzru'}, {'username':'UzRePort', 'title':'Uzreport Rasmiy', 'about':"UZREPORT telekanalining telegramdagi rasmiy futbol sahifasi.\nTakliflaringizni @FUTBOLTV1BOT ga jo'nating"}]
    return render_template("/index.html", channels = CHANNELS)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
    #     global HASH
    #     phone = request.form.get("phone")
    #     rows = db.execute("SELECT * FROM users WHERE phone = ?", phone)
    #     if not phone or rows:
    #         return apology("Phone is not available")

    #     password = request.form.get("password")
    #     if not password:
    #         return apology("missing password")

    #     confirmation = request.form.get("confirmation")
    #     if password != confirmation:
    #         return apology("passwords don`t match")

    #     session['phone'] = phone
    #     HASH = generate_password_hash(password)

        return send_verification()
    else:
        return render_template('/register.html')


@app.route("/send_verification", methods=["POST"])
def send_verification():
    # try:
    #     loop.run_until_complete(send_code_request())
    # except (PhoneNumberInvalidError, TypeError):
    #     loop.run_until_complete(disconnect_client())
    #     return apology('Invalid phone number', 401)
    # except SendCodeUnavailableError as e:
    #     loop.run_until_complete(disconnect_client())
    #     return apology('Verification code unavailable', 401)
    # except FloodWaitError as e:
    #     loop.run_until_complete(disconnect_client())
    #     return apology(f'Too many requests, please wait {e.seconds} seconds')
    return render_template("/confirm.html")


@app.route("/confirm", methods=["POST", "GET"])
def confirm():
    if request.method == "POST":
    #     global CHATS
    #     code = request.form.get("confirm")
    #     if not code:
    #         return apology("missing verification code")
    #     try:
    #         loop.run_until_complete(sign_in(session['phone'], code))
    #     except PhoneCodeInvalidError as e:
    #         loop.run_until_complete(disconnect_client())
    #         return apology("invalid validation code")
    #     db.execute("INSERT INTO users (phone, hash) VALUES(?, ?)", session['phone'], HASH)
    #     user_id = db.execute("SELECT id FROM users WHERE phone = ?", session['phone'])[0]['id']
    #     CHATS = loop.run_until_complete(get_public_channels())

    #     for chat in CHATS:
    #         id = db.execute("SELECT channel_id FROM channels WHERE username = ?", chat)
    #         if not id:
    #             if not chat: return apology(CHATS[0])
    #             db.execute("INSERT INTO channels (username) VALUES(?)", chat)
    #         id = db.execute("SELECT channel_id FROM channels WHERE username = ?", chat)[0]["channel_id"]
    #         db.execute("INSERT INTO followings (channel_id, user_id) VALUES(?, ?)", id, user_id)
        return render_template("/registered.html")
    else:
        return render_template("/confirm.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    # """Log user in"""
    # # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
    #     global BEGIN
    #     # Ensure phone number was submitted
    #     if not request.form.get("phone"):
    #         return apology("must provide phone", 403)

    #     # Ensure password was submitted
    #     elif not request.form.get("password"):
    #         return apology("must provide password", 403)

    #     # Query database for phone
    #     rows = db.execute("SELECT * FROM users WHERE phone = ?", request.form.get("phone"))

    #     # Ensure phone exists and password is correct
    #     if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
    #         return apology("invalid phone and/or password", 403)

    #     user_id = rows[0]['id']
    #     session['user_id'] = user_id

    #     BEGIN = session.get('last_time')
    #     if not BEGIN:
    #         yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    #         BEGIN = yesterday.strftime("(%Y, %m, %d, %H, %M, %S)")

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("/login.html")


@app.route("/messages", methods=["POST", "GET"])
def show_messages():
    if request.method == "POST":
        global DATA
        DATA = pd.read_csv('data.csv')
        DATA['date'] = pd.to_datetime(DATA['date'])
        DATA['text'] = DATA['text'].apply(lambda x: x.replace('\n', ' '))
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