from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from email_validator import validate_email, EmailNotValidError

from helpers import apology, login_required, admin_required, add_edit_items, return_usa_states
import datetime
import math

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['STATIC_FOLDER'] = 'static'
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///burger_data.db")

# Create tables necessary for saving user data
db.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        username TEXT NOT NULL,
        hash TEXT NOT NULL
    )
""")

db.execute("""
    CREATE UNIQUE INDEX IF NOT EXISTS username ON users (username)
""")

# Creates table for menu items
db.execute("""
    CREATE TABLE IF NOT EXISTS menu (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        price INTEGER NOT NULL,
        categoryId INTEGER NOT NULL,
        image_url TEXT NOT NULL
    )
""")

# Creates table for item categories (Burgers, sides...)
db.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        category TEXT NOT NULL

    )
""")

# Creates table for each of the items orders by users
db.execute("""
    CREATE TABLE IF NOT EXISTS user_order (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        userId INTEGER NOT NULL,
        itemId INTEGER NOT NULL,
        amount INTEGER NOT NULL
    )
""")

# Creates table for storing user admins
db.execute("""
    CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        userId INTEGER NOT NULL
    )
""")


@app.after_request
def after_request(response):
    """Ensure responses arent cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Global variable
ORDER_LIMIT = 5 # Sets maximum allowed limit for each order

# Context processor allows is_admin and order_number to be avaliable to all .html files
@app.context_processor
def admin_navbar():
    # This is necessary to show additional information in the navbar if the user is a admin
    is_admin = db.execute("SELECT * FROM users JOIN admins ON users.id = admins.userId WHERE users.id = ?;", session.get('user_id'))
    # And for all pages to track the amount of items the user has in his cart
    order_number = db.execute("SELECT SUM(amount) FROM user_order WHERE userId = ?", session.get('user_id'))[0]['SUM(amount)'] or 0
    return dict(is_admin=is_admin, order_number=order_number)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Get form data
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        usrExists = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Validate form data
        if not username or not password:
            return apology("Must provide email and password")
        elif password != confirmation:
            return apology("Password and confirmation fields do not match")
        elif usrExists:
            return apology("Invalid username: already exists!")
        elif len(password) < 8:
            return apology("Password must contain 8 characters or more")

        # Validate email with email_validator library
        try:
            v = validate_email(username)
            username = v.email
        except EmailNotValidError as e:
            return apology(str(e))

        # Hash password with werkzeug.security
        hashPassword = generate_password_hash(password)

        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hashPassword)
        usr = db.execute("SELECT * FROM users WHERE username = ?", username)[0]

        session["user_id"] = usr["id"]

        return redirect("/")

    return render_template("/register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide Email", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
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


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/menu")
def menu():
    # Get menu items and join the categories table necessary for filtering by category
    menu = db.execute("SELECT menu.*, categories.category FROM menu JOIN categories ON menu.categoryId = categories.id")
    categories = db.execute("SELECT category FROM categories")
    return render_template("menu.html", menu=menu, categories=categories)


@app.route("/burger/<int:burger_id>", methods=["GET", "POST"])
def burger_detail(burger_id):
    userIsLoggedIn = session.get('user_id')
    # Adds burger to user order
    if request.method == "POST" and userIsLoggedIn:  # did not use @login_required as I only want the POST route to be blocked for not registed users
        item = db.execute("SELECT * FROM user_order WHERE userId = ? AND itemId = ?", userIsLoggedIn, burger_id)

        # if the burger exists And its less than 5 (order limit)
        if item and item[0]['amount'] < ORDER_LIMIT:
            # We updated the count
            db.execute("UPDATE user_order SET amount = amount + 1 WHERE userId = ? AND itemId = ?", userIsLoggedIn, burger_id)
        # Else we insert a new user order with an amount of 1
        else:
            db.execute("INSERT INTO user_order (userId, itemId, amount) VALUES (?, ?, ?)", userIsLoggedIn, burger_id, 1)

        return redirect('/order')

    burger = db.execute("SELECT * FROM menu WHERE id == ?", burger_id)[0]
    return render_template("burger-detail.html", burger=burger, userIsLoggedIn=userIsLoggedIn)


@app.route("/order", methods=["GET", "POST"])
@login_required
def order():
    userId = session["user_id"]
    if request.method == "POST":
        # Use request.json to parse JSON data
        data = request.json
        order_id = data['orderId']
        new_amount = data['quantity']

        # If we get this specifc order_id we delete all orders from users order
        if order_id == 'clear-order' and new_amount == 0:
            db.execute("DELETE FROM user_order WHERE userId = ?", userId)
        # Update table with the new quantity
        elif new_amount <= ORDER_LIMIT and new_amount >= 1:
            db.execute("UPDATE user_order SET amount = ? WHERE userId = ? AND itemId = ?", new_amount, userId, order_id)
        # If the amount is equal to 0 we delete the item from the users orer
        elif new_amount == 0:
            db.execute("DELETE FROM user_order WHERE userId = ? AND itemId = ?", userId, order_id)

    orders = db.execute("SELECT * FROM user_order JOIN menu ON user_order.itemId = menu.id WHERE user_order.userId = ?", userId)

    return render_template("order.html", orders=orders)


@app.route("/checkout")
@login_required
def checkout():
    userId = session['user_id']
    orders = db.execute("SELECT * FROM user_order JOIN menu ON user_order.itemId = menu.id WHERE user_order.userId = ?", userId)

    # if the users order is empty we deny access to the page
    if not orders:
        return apology("Access Denied")

    # Calculate total order price
    total = 0.00
    for order in orders:
        total += order['price'] * order['amount']

    # Get the current year from 'import datetime'
    current_year = datetime.datetime.now().year

    return render_template("checkout.html", current_year=current_year, orders=orders, total=total, states=return_usa_states())


@app.route("/order-successful", methods=["GET", "POST"])
@login_required
def order_successful():
    current_year = datetime.datetime.now().year

    if request.method == "POST":
        # Get user billig information

        # User info
        name = request.form.get("name")
        surname = request.form.get("surname")
        address = request.form.get("address")
        city = request.form.get("city")
        state = request.form.get("state")
        zip_code = request.form.get("zip-code")

        # Credit card info
        payment_method = request.form.get("payment-method")
        card_number = request.form.get("card-number")
        month = request.form.get("month")
        year = request.form.get("year")
        security_code = request.form.get("security-code")

        # Check for empty Input
        if not name or not surname or not address or not city or not state or not zip_code:
            return apology("Invalid input, be sure to fill all required entries!")

        # Validate card expiration date
        month = int(month)
        year = int(year)
        if month < 1 or month > 12 or year < current_year:
            return apology("Invalid card expiration date")

        # Validate card number
        # Adapted the code from cs50 exercise 'sentimental-credit'.
        card_length = len(card_number)
        security_code_length = len(security_code)

        if payment_method == "mastercard":
            if card_length != 16 or security_code_length != 3:
                return apology("Invalid MasterCard number")
        elif payment_method == "visa":
            if card_length != 13 and card_length != 16 or security_code_length != 3:
                return apology("Invalid Visa number")
        elif payment_method == "amex":
            if card_length != 15 or security_code_length != 4:
                return apology("Invalid American Express number")

        card_number_copy = int(card_number)
        sum = 0
        sum_of_other_digits = 0

        # Hans Peter Luhn algorithm
        for x in range(card_length):
            if (x % 2) != 0:
                num = card_number_copy % 10
                multiply = num * 2

                if multiply > 9:
                    first = math.floor(multiply / 10)
                    last = multiply % 10
                    sum = sum + first + last
                else:
                    sum += multiply
            else:
                sum_of_other_digits += card_number_copy % 10

            card_number_copy /= 10
            card_number_copy = math.floor(card_number_copy)

        # If user is valid...
        if (sum + sum_of_other_digits) % 10 == 0:
            # Clear users order
            user_id = session['user_id']
            db.execute("DELETE FROM user_order WHERE userId = ?", user_id)

            return render_template("order-successful.html")
        else:
            return apology(f"Invalid {payment_method} number")

    return redirect("/")


# Admin Routes
@app.route("/admin-items")
@login_required
@admin_required
def admin_items():
    menu = db.execute("SELECT menu.*, categories.category FROM menu JOIN categories ON menu.categoryId = categories.id")
    categories = db.execute("SELECT category FROM categories")
    return render_template("admin/items.html", menu=menu, categories=categories)

# Delete item from menu table


@app.route("/admin-items/delete/<int:burger_id>", methods=["GET", "POST"])
@login_required
@admin_required
def admin_delete_item(burger_id):
    if request.method == "POST":
        db.execute("DELETE FROM menu WHERE id = ?", burger_id)

    return redirect("/admin-items")


# Edit existing item from menu table
@app.route("/admin-items/edit/<int:burger_id>", methods=["GET", "POST"])
@login_required
@admin_required
def admin_edit_item(burger_id):
    if request.method == "POST":
        # code for editing and adding items were very similar, so I made add_edit_items defined in helpers.py
        return add_edit_items("edit", burger_id)

    item = db.execute("SELECT * FROM menu WHERE menu.id = ?", burger_id)[0]
    categories = db.execute("SELECT * FROM categories")

    return render_template("/admin/edit-item.html", item=item, categories=categories)


# Insert new item into table menu
@app.route("/admin-items/add", methods=["GET", "POST"])
@login_required
@admin_required
def admin_add_item():
    if request.method == "POST":
        return add_edit_items("add")

    categories = db.execute("SELECT * FROM categories")
    return render_template("/admin/add-item.html", categories=categories)


@app.route("/admin-users", methods=["GET", "POST"])
@login_required
@admin_required
def admin_users():
    admins = db.execute("SELECT users.id, users.username FROM admins JOIN users ON admins.userId = users.id")
    return render_template("/admin/users.html", admins=admins)


# Deletes user from admin table
@app.route("/admin-users/delete/<int:admin_id>", methods=["GET", "POST"])
@login_required
@admin_required
def admin_users_delete(admin_id):
    if request.method == "POST":
        db.execute("DELETE FROM admins WHERE userId = ?", admin_id)

    return redirect("/admin-users")

# Adds new user to admin table
@app.route("/admin-users/add", methods=["GET", "POST"])
@login_required
@admin_required
def admin_add_user():
    if request.method == "POST":
        username = request.form.get("username")
        username_id = db.execute("SELECT id FROM users WHERE username = ? ", username)
        username_admin_id = db.execute(
            "SELECT users.id FROM users JOIN admins ON users.id = admins.userId WHERE users.username = ?", username)

        # Check if the email is a registered account
        if not username_id:
            return apology(f"No user found with the username: {username}")
        # Check if email is already an admin
        elif username_admin_id:
            return apology("User is already an admin !")
        # If all checks are passed we add the user to the admin table
        else:
            db.execute("INSERT INTO admins (userId) VALUES (?)", username_id[0]['id'])

    return redirect("/admin-users")
