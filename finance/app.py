import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


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
    """Show portfolio of stocks"""
    purchases = db.execute("SELECT * FROM purchase WHERE user_id = ?", session["user_id"])
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

    return render_template("/index.html", user={"cash": cash, "total": session["total"]}, purchases=purchases)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        stock = lookup(symbol)
        if not stock:
            return apology("invalid symbol")

        shares = request.form.get("shares")
        try:
            shares = int(shares)
        except:
            return apology("value must be greater than or equal to 1")
        if not shares or shares < 1:
            return apology("value must be greater than or equal to 1")

        cash = float(db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"])
        price = float(stock["price"])

        cash -= shares * price
        if cash < 0:
            return apology("can`t afford")

        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, session["user_id"])
        db.execute("INSERT INTO purchase (symbol, name, shares, price, user_id) VALUES(?, ?, ?, ?, ?)", symbol, stock["name"], shares, price, session["user_id"])
        return redirect("/")

    else:
        return render_template("/buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        session["total"] = rows[0]["cash"]
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        quoted = lookup(request.form.get("symbol"))
        if not quoted:
            return apology("invalid symbol")
        return render_template("/quoted.html", quoted=quoted)

    else:
        return render_template("/quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if not username or rows:
            return apology("Username is not available")

        password = request.form.get("password")
        if not password:
            return apology("missing password")

        confirmation = request.form.get("confirmation")
        if password != confirmation:
            return apology("passwords don`t match")

        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, generate_password_hash(password))
        return render_template("/login.html")
    else:
        return render_template("/register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        symbols = [i["symbol"] for i in db.execute("SELECT DISTINCT(symbol) FROM purchase")]
        return render_template("/sell.html", symbols=symbols)
    else:
        selected = request.form.getlist("symbol")[0]
        if not selected:
            return apology("missing symbol")

        owned = db.execute("SELECT * FROM purchase WHERE symbol = ?", selected)
        if not owned:
            return apology("invalid symbol")
        owned_number = int(owned[0]["shares"])

        shares = request.form.get("shares")
        try:
            shares = int(shares)
        except:
            return apology("value must be greater than or equal to 1")
        if not shares or shares > owned_number:
            return apology("too many shares")

        price = float(lookup(selected)["price"])
        db.execute("UPDATE purchase SET shares = ? WHERE id = ?", owned_number - shares, owned[0]["id"])

        cash = float(db.execute("SELECT cash FROM users WHERE id = ?", owned[0]["user_id"])[0]["cash"])
        cash += shares * price
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, owned[0]["user_id"])
        return redirect("/")