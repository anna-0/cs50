import os
from functools import wraps
from tempfile import mkdtemp
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
import gocardless_pro
from werkzeug.security import check_password_hash, generate_password_hash
from dotenv import load_dotenv
load_dotenv()

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

access_token = os.getenv('GC_ACCESS_TOKEN')

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///patrons.db")

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure email was submitted
        if not request.form.get("email"):
            return "<script>alert('Must provide email')</script>"

        # Ensure password was submitted
        elif not request.form.get("password"):
            return "<script>alert('Must provide password')</script>"

        # Query database for email
        rows = db.execute("SELECT * FROM users WHERE email = :email",
                          email=request.form.get("email"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return "<script>alert('Invalid email and/or password')</script>"

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["email"] = rows[0]["email"]
        session["ispatron"] = rows[0]["ispatron"]

        # Redirect user to home page
        return redirect("/loggedin")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    if request.method == "POST":

        # Gets user info and ensures proper usage
        email = request.form.get("email")
        password = request.form.get("password")

        if not email:
            return "<script>alert('Must provide email address')</script>"

        elif not password:
            return "<script>alert('Must provide password')</script>"

        elif password != request.form.get("confirmation"):
            return "<script>alert('Passwords do not match')</script>"

        # Checks if username exists
        rows = db.execute("SELECT * FROM users WHERE email = :email",
                          email=email)
        if len(rows) != 0:
            return "<script>alert('Email address already registered')</script>"

        else:
            # Makes hash of password
            passhash = generate_password_hash(password)

            # Inserts into users table
            db.execute("INSERT INTO users(email, hash) VALUES(:email, :password)",
                       email=email, password=passhash)

            # Stores user id as current session id
            session["user_id"] = db.execute("SELECT id FROM users WHERE email=:email", email=email)[0]["id"]
            session["email"] = db.execute("SELECT email FROM users WHERE email=:email", email=email)[0]["email"]
            session["ispatron"] = db.execute("SELECT ispatron FROM users WHERE email=:email", email=email)[0]["ispatron"]


            flash("Registered!")

            return redirect("/")

    else:
        return render_template("register.html")

@app.route("/")
def index():

    client = gocardless_pro.Client(
        access_token=access_token,
        environment='sandbox'
        )

    # Gets record lists from GC
    customers = client.customers.list().records
    mandates = client.mandates.list().records
    subscrips = client.subscriptions.list().records

    # Initialises variables to plug into page
    total = 0
    donors = 0
    names = []

    # Loops through subscriptions on GC to count up monthly total of subscription donations, skipping if cancelled
    for subscrip in subscrips:
        if subscrip.status == 'cancelled':
            continue
        donors += 1
        monthlyamount = format(subscrip.amount)
        total += int(monthlyamount)

        # Connects via subscriptions to mandates using their IDs, and then to customers via mandates using customer IDs
        for mandate in mandates:
            if mandate.id != subscrip.links.mandate:
                continue
            for customer in customers:
                if mandate.links.customer != customer.id:
                    continue

                # Pulls out names and plugs into name array
                firstname = customer.given_name
                lastname = customer.family_name
                name = firstname + ' ' + lastname[0]
                names.append(name)

    # Formats monthly total back to float from GC int
    monthlytotal = total / 100

    return render_template("index.html", donors=donors, names=names, monthlytotal=monthlytotal)


@app.route("/loggedin")
@app.route("/")
@login_required
def loggedin():

    client = gocardless_pro.Client(
        access_token=access_token,
        environment='sandbox'
        )

    # Gets record lists from GC
    customers = client.customers.list().records
    mandates = client.mandates.list().records
    subscrips = client.subscriptions.list().records

    # Initialises variables to plug into page
    total = 0
    donors = 0
    names = []
    GCemails = []

    # Loops through subscriptions on GC to count up monthly total of subscription donations, skipping if cancelled
    for subscrip in subscrips:
        if subscrip.status == 'cancelled':
            continue
        donors += 1
        monthlyamount = (format(subscrip.amount))
        total += int(monthlyamount)

        # Connects via subscriptions to mandates using their IDs, and then to customers via mandates using customer IDs
        for mandate in mandates:
            if mandate.id != subscrip.links.mandate:
                continue
            for customer in customers:
                if mandate.links.customer != customer.id:
                    continue

                # Pulls out names and plugs into name array
                firstname = customer.given_name
                lastname = customer.family_name
                name = firstname + ' ' + lastname[0]
                names.append(name)
                GCemails.append(customer.email)

    if session["email"] in GCemails:
        db.execute("UPDATE users SET ispatron = 1 WHERE id=:user_id", user_id=session["user_id"])
        session["ispatron"] = 1

    # Formats monthly total back to float from GC int
    monthlytotal = total / 100

    return render_template("index.html", donors=donors, names=names, monthlytotal=monthlytotal)

@app.route("/mysubscription")
@login_required
def mysubscription():

    client = gocardless_pro.Client(
        access_token=access_token,
        environment='sandbox'
        )

    # Gets record lists from GC
    customers = client.customers.list().records
    mandates = client.mandates.list().records
    subscrips = client.subscriptions.list().records

    mysubs = 0
    dict = {'email': '', 'amount': ''}

    # Loops through subscriptions on GC to count up monthly total of subscription donations, skipping if cancelled
    for subscrip in subscrips:
        if subscrip.status == 'cancelled':
            continue
        dict['amount'] = (format(subscrip.amount))
        # Connects via subscriptions to mandates using their IDs, and then to customers via mandates using customer IDs
        for mandate in mandates:
            if mandate.id != subscrip.links.mandate:
                continue
            for customer in customers:
                if mandate.links.customer != customer.id:
                    continue
                # Pulls out names and plugs into name array
                dict['email'] = customer.email

                if dict['email'] == session["email"]:
                    mysubs = int(int(dict['amount']) / 100)


    return render_template("mysubscription.html", mysubs=mysubs)

@app.route("/behindthescenes")
@login_required
def behindthescenes():

    return render_template("behindthescenes.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")