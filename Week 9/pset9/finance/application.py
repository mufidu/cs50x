import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd, usd

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
    username = db.execute("SELECT username FROM users WHERE id = :uid", uid=int(session['user_id']))[0]["username"]

    stocks = db.execute("SELECT symbol, shares FROM portfolio WHERE username = :username", username=username)

    total_sum = []

    for stock in stocks:
        symbol = str(stock["symbol"])
        shares = int(stock["shares"])
        name = lookup(symbol)["name"]
        price = lookup(symbol)["price"]
        total = shares * price
        stock["name"] = name
        stock["price"] = usd(price)
        stock["total"] = usd(total)
        total_sum.append(float(total))

    cash_available = db.execute("SELECT cash FROM users WHERE username = :username", username=username)[0]["cash"]
    cash_total = sum(total_sum) + cash_available

    return render_template("index.html", stocks=stocks, cash_available=usd(cash_available), cash_total=usd(cash_total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        # Store the dictionary returned from the search in a variable
        look = lookup(request.form.get("symbol"))

        # Store the shares inputed
        shares = request.form.get("shares")

        # If the symbol searched or number of shares is invalid, return apology
        if look == None:
            return apology("invalid symbol", 400)
        elif not shares.isdigit() or int(shares) < 1:
            return apology("share must be at least 1", 400)

        # Store how much money the user has
        cash = db.execute("SELECT cash FROM users WHERE id = :uid", uid=int(session['user_id']))

        # Store the value of purchase
        value = look["price"] * int(shares)

        # If the user don't have enough money, apologize
        if int(cash[0]["cash"]) < value:
            return apology("You don't have enough money to proceed", 403)

        # If the user can afford the purchase, proceed
        else:
            # Subtract the value of purchase from the user's cash
            db.execute("UPDATE users SET cash = cash - :value WHERE id = :uid", value=value, uid=int(session['user_id']))

            # Add the transaction to the user's history
            db.execute("INSERT INTO history (username, operation, symbol, price, shares) VALUES (:username, 'BUY', :symbol, :price, :shares)",
                       username=db.execute("SELECT username FROM users WHERE id = :user_id",
                                           user_id=int(session['user_id']))[0]["username"],
                       symbol=look['symbol'], price=look['price'], shares=request.form.get('shares'))

            # Add the stock to the user's portfolio
            db.execute("INSERT INTO portfolio (username, symbol, shares) VALUES (:username, :symbol, :shares)",
                       username=db.execute("SELECT username FROM users WHERE id = :user_id",
                                           user_id=int(session['user_id']))[0]["username"],
                       symbol=look['symbol'], shares=request.form.get('shares'))

            # Send them to the portfolio
            return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # save username
    username = db.execute("SELECT username FROM users WHERE id = :uid", uid=int(session['user_id']))[0]["username"]

    # save history to list
    stocks = db.execute(
        "SELECT operation, symbol, price, date, time, shares FROM history WHERE username = :username", username=username)

    for stock in stocks:
        symbol = str(stock["symbol"])
        name = lookup(symbol)["name"]
        stock["name"] = name

    return render_template("history.html", stocks=stocks)


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
    if request.method == 'GET':
        return render_template("quote.html")
    else:
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("no symbol")
        stock = lookup(symbol)
        stock["price"] = usd(stock["price"])
        return render_template("quoted.html", stock=stock)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # set variables
    username = request.form.get("username")
    password = request.form.get("password")
    if request.method == "GET":
        return render_template("register.html")
    else:
        if not request.form.get("username"):
            return apology("Missing username!", 400)
        elif password != request.form.get("confirmation"):
            return apology("Passwords do not match!", 400)
        else:
            # hash the password
            hash = generate_password_hash(password)
            # add user to database, checking to make sure they are not already registered
            success = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=username, hash=hash)
            if not success:
                return apology("Username already exists")
            # log them in
            rows = db.execute("SELECT id FROM users WHERE username = :username", username=username)
            if not rows:
                return apology("Query failed")
            session["user_id"] = rows[0]["id"]
            return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # save uname
    username = db.execute("SELECT username FROM users WHERE id = :uid", uid=int(session['user_id']))[0]["username"]

    if request.method == "POST":
        look = lookup(request.form.get("symbol"))
        shares = request.form.get("shares")

        # save total shares
        user_shares = db.execute("SELECT shares FROM portfolio WHERE username = :username and symbol = :symbol",
                                 username=username, symbol=str(request.form.get("symbol")))[0]["shares"]

        # save values of shares
        value = look["price"] * int(shares)

        # apologies
        if not request.form.get("symbol") or look == None:
            return apology("no stock", 400)
        elif not shares or not shares.isdigit() or int(shares) < 1 or int(shares) > int(user_shares):
            return apology("share num error", 400)

        # start selling
        else:
            # valuing
            db.execute("UPDATE users SET cash = cash + :value WHERE id = :user_id", value=value, user_id=int(session['user_id']))

            # adding to history
            db.execute("INSERT INTO history (username, operation, symbol, price, shares) VALUES (:username, 'SELL', :symbol, :price, :shares)",
                       username=username, symbol=look['symbol'], price=look['price'], shares=request.form.get('shares'))

            # removing (if all sold)
            if int(user_shares) == int(shares):
                db.execute("DELETE FROM portfolio WHERE username = :username and symbol = :symbol",
                           username=username, symbol=str(request.form.get("symbol")))

            # updating (if not all sold)
            elif int(user_shares) > int(shares):
                db.execute("UPDATE portfolio SET shares = :shares WHERE username = :username and symbol = :symbol",
                           shares=shares, username=username, symbol=request.form.get("symbol"))

        # redirect to home
        return redirect("/")

    elif request.method == "GET":
        symbols = db.execute("SELECT symbol FROM portfolio WHERE username = :username", username=username)
        return render_template("sell.html", symbols=symbols)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
