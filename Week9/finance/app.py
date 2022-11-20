import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

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
    id = session["user_id"]
    portfolio = db.execute("SELECT * FROM portfolio WHERE id = ?", id)
    balance = db.execute("SELECT cash FROM users WHERE id = ?", id)
    balance = balance[0]["cash"]
    total = 0
    # add all owned stocks
    for stock in portfolio:
        stock_total = stock["price"] * stock["shares"]
        total += float(stock_total)
    total += float(balance)
    total = usd(total)
    balance = usd(balance)
    return render_template("index.html", portfolio=portfolio, balance=balance, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")

    if request.method == "POST":
        # info from form
        stock = lookup(request.form.get("symbol"))
        shares = request.form.get("shares")
        try:
            shares = int(shares)
        except ValueError:
            return apology("shares must be a whole number")
        # invalid stock apology
        if stock == None:
            return apology("stock symbol invalid")
        # negative shares apology
        elif shares <= 0:
            return apology("number of shares must be a number greater than 0")
        else:
            id = session["user_id"]
            symbol = stock["symbol"]
            price = stock["price"]
            name = stock["name"]
            # calculate cost of transaction
            cost = price * shares

            # query user cash balance
            balance = db.execute("SELECT cash FROM users WHERE id = ?", id)
            balance = balance[0]["cash"]

            # check account has enough cash
            if cost > balance:
                return apology("not enough cash in account")

            # complete buy
            else:
                # add to transaction history
                time = datetime.datetime.now()
                db.execute("INSERT INTO transactions (id, symbol, shares, price, time) VALUES (?, ?, ?, ?, ?)",
                           id, symbol, shares, price, time)

                # check if own shares already
                owned = db.execute("SELECT shares FROM portfolio WHERE id = ? AND symbol = ?", id, symbol)

                # add new shares to portfolio
                if len(owned) > 0:
                    owned = (owned[0]["shares"])
                    shares = shares + owned
                    db.execute("UPDATE portfolio SET shares = ? WHERE id = ? AND symbol = ?", shares, id, symbol)
                else:
                    db.execute("INSERT INTO portfolio (id, symbol, name, shares, price) VALUES (?, ?, ?, ?, ?)",
                               id, symbol, name, shares, price)

                # update balance
                balance -= cost
                db.execute("UPDATE users SET cash = ? WHERE id = ?", balance, id)
                flash("Bought!")
                return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    id = session["user_id"]
    transactions = db.execute("SELECT * FROM transactions WHERE id = ?", id)
    return render_template("history.html", transactions=transactions)


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
    if request.method == "GET":
        return render_template("quote.html")

    if request.method == "POST":
        stock = lookup(request.form.get("symbol"))

        # Stock invalid
        if stock == None:
            return apology("stock symbol invalid")
        # Show stock quote
        else:
            return render_template(
                "quoted.html",
                name=stock["name"],
                symbol=stock["symbol"],
                price=usd(stock["price"]))


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # field left blank
        if not username or not password or not confirmation:
            return apology("must provide all fields")

        # username taken
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) != 0:
            return apology("username already taken")

        # password and confirmation do not match
        if password != confirmation:
            return apology("passwords do not match")

        # make password secure in database
        hash = generate_password_hash(password)

        # Insert user info into db
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)

        # Redirect user to login page
        return redirect("/login")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        id = session["user_id"]
        portfolio = db.execute("SELECT * FROM portfolio WHERE id = ?", id)
        return render_template("sell.html", portfolio=portfolio)

    if request.method == "POST":
        id = session["user_id"]
        sell_shares = request.form.get("shares")
        try:
            sell_shares = int(sell_shares)
        except ValueError:
            return apology("shares must be a whole number")
        stock = lookup(request.form.get("symbol"))

        symbol = stock["symbol"]
        price = stock["price"]

        # query users cash balance
        balance = db.execute("SELECT cash FROM users WHERE id = ?", id)
        balance = balance[0]["cash"]

        # query for owned stock to sell
        owned = db.execute("SELECT shares FROM portfolio WHERE id = ? AND symbol = ?", id, symbol)
        # invalid inputs to form
        if stock == None:
            return apology("stock symbol invalid")
        elif sell_shares <= 0:
            return apology("number of shares much be greater than 0")

        # specified stock or share amount not owned
        elif len(owned) == 0:
            return apology("no shares from this company")
        elif owned[0]["shares"] < sell_shares:
            return apology("not enough shares")

        # make sale
        else:
            new_shares = int(owned[0]["shares"]) - sell_shares
            profit = price * sell_shares
            balance += profit

            # sold all shares, remove from portfolio
            if new_shares == 0:
                db.execute("DELETE FROM portfolio WHERE id = ? AND symbol = ?", id, symbol)
                db.execute("UPDATE users SET cash = ? WHERE id = ?", balance, id)

            # sold portion of shares, update portfolio & cash balance
            else:
                db.execute("UPDATE portfolio SET shares = ? WHERE id = ? AND symbol = ?", new_shares, id, symbol)
                db.execute("UPDATE users SET cash = ? WHERE id = ?", balance, id)

            # add to transaction history
            shares = sell_shares * (-1)
            time = datetime.datetime.now()
            db.execute("INSERT INTO transactions (id, symbol, shares, price, time) VALUES (?, ?, ?, ?, ?)",
                       id, symbol, shares, price, time)

            flash("Sold!")
            return redirect("/")