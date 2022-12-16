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
db = SQL("sqlite:///library.db")

# Make sure API key is set
# if not os.environ.get("API_KEY"):
#     raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    id = session["user_id"]
    """Show personal library"""
    if request.method == "GET":
        id = session["user_id"]
        shelf = db.execute("SELECT * FROM shelf WHERE id = ?", id)
        return render_template("index.html", shelf=shelf)

    if request.method == "POST":
        title = request.form.get("title")
        status = request.form.get("status")
        db.execute("UPDATE shelf SET status = ? WHERE id = ? AND title = ?", status, id, title)


@app.route("/log", methods=["GET", "POST"])
@login_required
def log():
    """Log reading"""
    if request.method == "GET":
        id = session["user_id"]
        shelf = db.execute("SELECT * FROM shelf WHERE id = ?", id)
        return render_template("log.html", shelf=shelf)

    if request.method == "POST":
        # info from form
        title = request.form.get("title")
        pages = request.form.get("pages")
        author = request.form.get("author")
        pageCount = int(request.form.get("pageCount"))
        pagesRead = int(request.form.get("pagesRead"))
        pagesSession = int(pages) - int(pagesRead)

        try:
            pages = int(pages)
        except ValueError:
            return apology("Pages must be a whole number")
        # invalid title apology
        if title == None or title == "":
            return apology("Title invalid")
        # negative pages apology
        elif pages <= 0:
            return apology("Number of pages must be a number greater than 0")
        elif pages > pageCount:
            return apology("Number of pages read exceeds book's page count")
        elif pages <= pagesRead:
            return apology("Number of pages read must be larger than previous session to log")
        else:
            id = session["user_id"]

            # add to history
            date = request.form.get("date")
            if date == None or date == "":
                return apology("No date entered")

            db.execute("INSERT INTO log (id, title, author, pagesRead, pagesSession, date) VALUES (?, ?, ?, ?, ?, ?)",
                        id, title, author, pages, pagesSession, date)

            # update total read pages in shelf
            if pagesRead > 0:
                db.execute("UPDATE shelf SET pagesRead = ? WHERE id = ? AND title = ?", pages, id, title)
           # bookjust started -- update status to currently reading
            else:
                db.execute("UPDATE shelf SET pagesRead = ?, status = 'Currently Reading', startDate = ? WHERE id = ? AND title = ?", pages, date, id, title)
            # book finished -- update status to read
            if pages == pageCount:
                db.execute("UPDATE shelf SET status = 'Read', readDate = ? WHERE id = ? AND title = ?", date, id, title)

            flash("Reading Logged!")
            return redirect("/")


@app.route("/search",  methods=["GET", "POST"])
@login_required
def search_script():
    if request.method == "GET":
        return render_template("search.html")

    if request.method == "POST":
        id = session["user_id"]
        title = request.form.get("title")
        author = request.form.get("author")
        pageCount = request.form.get("pageCount")
        date = datetime.datetime.now()

        # check if already in library
        onshelf = db.execute("SELECT title FROM shelf WHERE id = ? AND title = ? AND author = ?", id, title, author)
        if len(onshelf) > 0:
            flash("Book already in library...")
        else:
            db.execute("INSERT INTO shelf (id, title, author, pageCount, addDate) VALUES (?, ?, ?, ?, ?)", id, title, author, pageCount, date)
            flash("Book added to library!")
    return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history"""
    id = session["user_id"]
    log = db.execute("SELECT * FROM log WHERE id = ?", id)
    return render_template("history.html", log=log)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Invalid username and/or password", 403)

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
            return apology("Must provide all fields")

        # username taken
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) != 0:
            return apology("Username already taken")

        # password and confirmation do not match
        if password != confirmation:
            return apology("Passwords do not match")

        # make password secure in database
        hash = generate_password_hash(password)

        # Insert user info into db
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)

        # Redirect user to login page
        return redirect("/login")

