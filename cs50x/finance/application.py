import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Gets user's stocks and cash info
    stocks = db.execute("SELECT symbol, SUM(shares) as totalshares FROM transactions WHERE user_id=:user_id GROUP BY symbol HAVING totalshares > 0",
                        user_id=session["user_id"])
    users = db.execute("SELECT cash FROM users WHERE id=:user_id",
                       user_id=session["user_id"])

    # Initialises cash, totals and list for parsing info
    cash = float(users[0]["cash"])
    total = 0

    stockinfo = []

    # Loops through stocks from db and stores values in list to be used in index.html
    for stock in stocks:
        # Gets symbol into a string
        symbol = str(stock["symbol"])
        # Gets number of shares owned
        shares = stock["totalshares"]
        # Looks up symbol to get name and price data
        quote = lookup(symbol)
        # Stores name as string
        name = str(quote["name"])
        # Stores price as float
        price = float(quote["price"])
        # Gets total price of stock
        shareprice = float(price * shares)
        # Increments to total
        total += shareprice
        # Appends data to list to allow carryover
        stockinfo.append({'symbol': symbol, 'shares': shares, 'name': name, 'price': price, 'total': shareprice})

    # Total amount including incremented prices
    totalval = total + cash

    return render_template("index.html", cash=cash, totalval=totalval, stockinfo=stockinfo)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":

        # Gets form inputs
        quote = lookup(request.form.get("symbol"))
        shares = request.form.get("shares")

        # Checks for symbol
        if quote == None:
            return apology("invalid symbol", 400)

        # Checks for proper usage
        if shares == '':
            return apology("please input number of shares", 400)
        else:
            shares = int(shares)

        rows = db.execute("SELECT cash FROM users WHERE id = :user_id",
                          user_id=session["user_id"])

        # Calculates if user has enough cash
        cashleft = rows[0]["cash"]
        sharecost = quote["price"]

        totalcost = sharecost * shares

        if totalcost > cashleft:
            return apology("insufficient funds")

        # Updates cash post-buy and inserts transaction into table
        db.execute("UPDATE users SET cash = cash - :price WHERE id = :user_id",
                   price=totalcost, user_id=session["user_id"])

        dt = datetime.now()
        history = dt.strftime("%Y-%m-%d %H:%M")
        db.execute("INSERT INTO transactions(user_id, symbol, shares, price, datetime) VALUES(:user_id, upper(:symbol), :shares, :price, :history)",
                   user_id=session["user_id"], symbol=request.form.get("symbol"), shares=shares, price=totalcost, history=history)

        flash("Bought!")

        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Brings out transaction data from table
    transactions = db.execute("SELECT symbol, shares, datetime FROM transactions WHERE user_id=:user_id ORDER BY datetime DESC",
                              user_id=session["user_id"])
    # Sets up dict
    stockinfo = {}

    # Loops through to get stock data
    for stock in transactions:
        stockinfo[stock["symbol"]] = lookup(stock["symbol"])

    return render_template("history.html", stockinfo=stockinfo, transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

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

    if request.method == "POST":

        # Checks symbol input
        quote = lookup(request.form.get("symbol"))

        if quote == None:
            return apology("invalid symbol", 400)

        return render_template("quoted.html", quote=quote)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    if request.method == "POST":

        # Gets user info and ensures proper usage
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return "<script>alert('Must provide username')</script>"

        elif not password:
            return "<script>alert('Must provide password')</script>"

        elif password != request.form.get("confirmation"):
            return "<script>alert('Passwords do not match')</script>"

        # Checks if username exists
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=username)
        if len(rows) != 0:
            return "<script>alert('Username not available')</script>"

        else:
            # Makes hash of password
            passhash = generate_password_hash(password)

            # Inserts into users table
            db.execute("INSERT INTO users(username, hash) VALUES(:username, :password)",
                       username=username, password=passhash)

            # Stores user id as current session id
            session["user_id"] = db.execute("SELECT id FROM users WHERE username=:username", username=username)[0]["id"]

            flash("Registered!")

            return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":

        # Gets input data and ensures proper usage
        shares = request.form.get("shares")
        quote = request.form.get("symbol")

        if quote == None:
            return apology("please select a symbol", 400)
        else:
            quote = lookup(quote)

        if shares == '':
            return apology("please input number of shares")
        # Stores number of shares as an int
        else:
            shares = int(shares)

        # Gets user's owned stocks
        prevstocks = db.execute("SELECT SUM(shares) AS totalshares FROM transactions WHERE symbol=:symbol AND user_id=:user_id GROUP BY symbol",
                                symbol=request.form.get("symbol"), user_id=session["user_id"])

        if prevstocks[0]["totalshares"] < shares:
            return apology("can only sell owned shares", 400)

        # Calculates stock worth
        price = quote["price"]

        totalprice = price * shares

        # Updates cash to post-sold amount
        db.execute("UPDATE users SET cash = cash + :price WHERE id = :user_id",
                   price=totalprice, user_id=session["user_id"])

        # Inserts transaction into history
        dt = datetime.now()
        history = dt.strftime("%Y-%m-%d %H:%M")
        db.execute("INSERT INTO transactions(user_id, symbol, shares, price, datetime) VALUES(:user_id, :symbol, :shares, :price, :history)",
                   user_id=session["user_id"], symbol=request.form.get("symbol"), shares=-shares, price=totalprice, history=history)

        flash("Sold!")

        return redirect("/")

    else:
        # Gets stocks to display in drop-down
        prevstocks = db.execute("SELECT symbol, SUM(shares) as totalshares FROM transactions WHERE user_id=:user_id GROUP BY symbol HAVING totalshares > 0",
                                user_id=session["user_id"])
        return render_template("sell.html", prevstocks=prevstocks)


@app.route("/addfunds", methods=["GET", "POST"])
@login_required
def addfunds():

    if request.method == "POST":

        # Gets desired amount
        amount = request.form.get("amount")

        # Updates cash accordingly
        db.execute("UPDATE users SET cash = cash + :amount WHERE id = :user_id",
                   amount=amount, user_id=session["user_id"])

        flash(f"Added ${amount} to funds")

        return redirect("/")

    else:
        return render_template("addfunds.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
