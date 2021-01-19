import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date

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
    stock_of_user = db.execute("SELECT * FROM purchases WHERE user_id=:user_id", user_id=session["user_id"])
    overall_total = float(db.execute("SELECT cash FROM users WHERE id=:id", id=session["user_id"])[0]["cash"])
    cash = overall_total
    for stock in stock_of_user:
        price = lookup(stock['stock'])['price']
        overall_total += price * stock["number"]
        db.execute("UPDATE purchases SET cost=:cost WHERE user_id=:user_id AND stock=:stock", cost=price, user_id=session["user_id"], stock=stock["stock"])
    updated_stocks = db.execute("SELECT * FROM purchases WHERE user_id=:user_id", user_id=session["user_id"])
    return render_template("index.html", cash=cash, overall_total=overall_total, updated_stocks=updated_stocks)

@app.route("/addcash", methods=["GET", "POST"])
@login_required
def addcash():
    """Show history of transactions"""
    if request.method == "POST":
        request.form.get("amount")
        db.execute("UPDATE users SET cash=cash+:totalcost WHERE id=:id", totalcost=float(request.form.get("amount")), id=session["user_id"])
    return redirect("/")

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")
    elif request.method == "POST":
        price = {}
        price = lookup(request.form.get("symbol"))
        if not request.form.get("symbol") or not price:
            return apology("Sorry, that symbol does not exist", 400)
        if not request.form.get("shares") or int(request.form.get("shares")) <= 0:
            return apology("You must enter a positive number of share", 400)
        totalcost = int(request.form.get("shares")) * price["price"]
        cash = db.execute("SELECT cash FROM users WHERE id=:id", id=session["user_id"])
        print(f"{cash}")
        if totalcost > cash[0]["cash"]:
            return apology("You do not have enough cash for this transaction")

        db.execute("UPDATE users SET cash=cash-:totalcost WHERE id=:id", totalcost=totalcost, id=session["user_id"]);
        # add transaction to transactions database
        today = date.today()
        transaction = db.execute("INSERT INTO transactions (user_id, stock, number, cost, date) VALUES (:user_id, :stock, :number, :cost, :date)", user_id = session["user_id"], stock=price["symbol"], number=int(request.form.get("shares")), cost=price["price"], date=today.strftime("%d/%m/%Y"))
        stocks_owned = db.execute("SELECT * FROM purchases")
        if not stocks_owned:
                db.execute("INSERT INTO purchases (user_id, stock, number, cost) VALUES (:user_id, :stock, :number, :cost)", user_id = session["user_id"], stock=price["symbol"], number=int(request.form.get("shares")), cost=price["price"])
        else:
            for stock in stocks_owned:
                if stock["stock"] == price["symbol"]:
                    number = stock["number"]
                    db.execute("UPDATE purchases SET number=number+:stock_number WHERE user_id=:user_id AND stock=:stock", stock_number=int(request.form.get("shares")), user_id=session["user_id"], stock=stock["stock"])
                else:
                    db.execute("INSERT INTO purchases (user_id, stock, number, cost) VALUES (:user_id, :stock, :number, :cost)", user_id = session["user_id"], stock=price["symbol"], number=int(request.form.get("shares")), cost=price["price"])
        return redirect("/")

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute("SELECT * FROM transactions")
    for transact in transactions:
        print(f"{transact}")
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
    elif request.method == "POST":
        price = {}
        price = lookup(request.form.get("symbol"))
        if not price:
            return apology("Sorry, that symbol does not exist")
        print(f"{price}")
        return render_template("quoted.html", companyname=price["name"], symbol=price["symbol"], cost=price["price"])



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        usernames = db.execute("SELECT username FROM users WHERE username=:username", username=request.form.get("username)"))
        if not request.form.get("username"):
            return apology("must provide username", 400)
        if usernames:
            return apology("username already exists", 400)
        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 400)
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 400)
        db.execute("INSERT INTO users (username,hash) VALUES(?,?)", request.form.get("username"), generate_password_hash(request.form.get("password")))
        return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        stocks = db.execute("SELECT stock FROM purchases WHERE user_id=:user_id", user_id=session["user_id"])
        return render_template("sell.html", stocks=stocks)
    elif request.method == "POST":
        price = {}
        price = lookup(request.form.get("symbol"))
        total_stocks = db.execute("SELECT number FROM purchases WHERE user_id=:user_id AND stock=:stock", user_id=session["user_id"], stock=request.form.get("symbol"))
        that_stock = 0
        for stock in total_stocks:
            that_stock += int(stock["number"])
        if not request.form.get("stock") or int(request.form.get("shares")) < 1:
            return apology("You must enter a positive number of shares and select a stock", 400)
        #totalcost = int(request.form.get("shares")) * price["price"]
        cash = db.execute("SELECT cash FROM users WHERE id=:id", id=session["user_id"])
        #print(f"{cash}")
        if that_stock < int(request.form.get("shares")):
            return apology("You do not have that many stocks")
        totalsell = int(request.form.get("shares")) * price["price"]
        db.execute("UPDATE users SET cash=cash+:totalsell WHERE id=:id", totalsell=totalsell, id=session["user_id"]);
        # add transaction to transactions database
        db.execute("UPDATE purchases SET number=number-:stock_number WHERE user_id=:user_id AND stock=:stock", stock_number=int(request.form.get("shares")), user_id=session["user_id"], stock=request.form.get("stock"))
        today = date.today()
        transaction = db.execute("INSERT INTO transactions (user_id, stock, number, cost, date) VALUES (:user_id, :stock, :number, :cost, :date)", user_id = session["user_id"], stock=price["symbol"], number=0-int(request.form.get("shares")), cost=price["price"], date=today.strftime("%d/%m/%Y"))
        return redirect("/")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
