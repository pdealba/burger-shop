from flask import redirect, render_template, session, request
from functools import wraps
from cs50 import SQL

db = SQL("sqlite:///burger_data.db")

def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


# Simlar to login_required, but checks if the user is an admin by looking through the admin table
def admin_required(f):
    """Decorate routes to require admin login."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        is_admin = db.execute("SELECT * FROM users JOIN admins ON users.id = admins.userId WHERE users.id = ?;", session['user_id'])

        if not is_admin:
            return apology("Unauthorized", 403)

        return f(*args, **kwargs)

    return wrapper


# Helper Function to add / edit menu items
def add_edit_items(type, burger_id=None):
    name = request.form.get("name")
    description = request.form.get("description")
    price = request.form.get("price")
    category = request.form.get("category")
    image_url = request.form.get("image-url")

    # Check if values are empty
    if name is not None and description is not None and price is not None and category is not None and image_url is not None:
        categoryId = db.execute("SELECT id FROM categories WHERE category = ?", category)[0]['id']
        if type == "edit":
            db.execute("UPDATE menu SET name = ?, description = ?, price = ?, categoryId = ?, image_url = ? WHERE id = ?", name, description, price, categoryId, image_url, burger_id)
        elif type == "add":
            db.execute("INSERT INTO menu (name, description, price, categoryId, image_url) VALUES (?, ?, ?, ?, ?)", name, description, price, categoryId, image_url)

    else:
        return apology("All entries must be filled!")

    return redirect("/admin-items")

# Returns array of all the states. The restaurant can modify the list according to their needs / availability
def return_usa_states():
    usa_states = [
        'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut',
        'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa',
        'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan',
        'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
        'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma',
        'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee',
        'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'
    ]
    return usa_states



