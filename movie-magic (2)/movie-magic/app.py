# ============================================================
# Movie Magic - Flask Movie Ticket Booking App
# ============================================================
# Run with: python app.py
# Visit: http://127.0.0.1:5000
# ============================================================

from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os

# Initialize the Flask app
app = Flask(__name__)

# Secret key for session management (change this in production!)
app.secret_key = "moviemagic_secret_key_2024"

# ─────────────────────────────────────────────
# SAMPLE DATA - In a real app, use a database
# ─────────────────────────────────────────────

# Simple in-memory user store (resets on server restart)
users = {}

# Movie data with details
MOVIES = [
    {
        "id": 1,
        "title": "Doomday",
        "genre": "Sci-Fi",
        "duration": "2h 18m",
        "rating": "U/A",
        "score": "9.1",
        "description": "Earth's last defense force faces a catastrophic alien countdown as a mysterious signal triggers a planet-wide doomsday sequence.",
        "price": 250,
        "times": ["10:30 AM", "1:45 PM", "5:00 PM", "8:15 PM"],
        "color": "#4F8EF7",
        "emoji": "🚀",
        "poster": "dooms.jpeg"
    },
    {
        "id": 2,
        "title": "The Paradise",
        "genre": "Thriller",
        "duration": "1h 58m",
        "rating": "A",
        "score": "8.7",
        "description": "A detective hunting a serial killer discovers the murders lead straight to the city's most glamorous and deadly secret society.",
        "price": 220,
        "times": ["11:00 AM", "2:30 PM", "6:00 PM", "9:00 PM"],
        "color": "#E84040",
        "emoji": "🔪",
        "poster": "paradise.jpeg"
    },
    {
        "id": 3,
        "title": "Peddi",
        "genre": "Drama",
        "duration": "2h 05m",
        "rating": "U",
        "score": "8.4",
        "description": "A resilient farmer's son fights against a corrupt landlord system to reclaim his family's land and dignity in rural Telangana.",
        "price": 180,
        "times": ["12:00 PM", "3:15 PM", "7:00 PM"],
        "color": "#3DBF6E",
        "emoji": "🌾",
        "poster": "peddi.jpeg"
    },
    {
        "id": 4,
        "title": "Dhurandhar-2",
        "genre": "Action",
        "duration": "2h 32m",
        "rating": "U/A",
        "score": "8.9",
        "description": "The legendary warrior Dhurandhar returns — this time taking on a vast arms smuggling empire threatening to destabilize the nation.",
        "price": 280,
        "times": ["10:00 AM", "1:00 PM", "4:30 PM", "8:00 PM", "10:45 PM"],
        "color": "#FF6A00",
        "emoji": "⚔️",
        "poster": "dhurandhar1.jpeg"
    },
    {
        "id": 5,
        "title": "Toxic",
        "genre": "Romance",
        "duration": "1h 52m",
        "rating": "U/A",
        "score": "8.2",
        "description": "Two passionate souls fall into a whirlwind romance — but their love is laced with secrets, obsession, and a dangerous past.",
        "price": 200,
        "times": ["11:30 AM", "2:00 PM", "5:30 PM", "8:30 PM"],
        "color": "#FF0080",
        "emoji": "🌹",
        "poster": "toxic.jpeg"
    },
    {
        "id": 6,
        "title": "The Conjuring",
        "genre": "Horror",
        "duration": "1h 52m",
        "rating": "A",
        "score": "8.6",
        "description": "Paranormal investigators are summoned to a farmhouse where an ancient demonic presence has terrorized a family for generations.",
        "price": 220,
        "times": ["12:30 PM", "4:00 PM", "7:30 PM", "10:00 PM"],
        "color": "#8800CC",
        "emoji": "👻",
        "poster": "conjuring.jpeg"
    },
]

# Booked seats storage: { "movie_id_theatre_showtime": ["A1", "B3", ...] }
booked_seats = {}

# ─── Theatre Data ───
THEATRES = [
    {
        "id": "pvr_kukatpally",
        "name": "PVR Cinemas",
        "location": "Kukatpally, Hyderabad",
        "logo": "🎦",
        "brand": "PVR",
        "facilities": ["Dolby Atmos", "4K", "Recliner Seats"],
        "color": "#e50914"
    },
    {
        "id": "pvr_jubilee",
        "name": "PVR ICON",
        "location": "Jubilee Hills, Hyderabad",
        "logo": "🎦",
        "brand": "PVR",
        "facilities": ["IMAX", "Dolby", "Premium Lounge"],
        "color": "#e50914"
    },
    {
        "id": "inox_gnfc",
        "name": "INOX Multiplex",
        "location": "GNFC Info Tower, Hyderabad",
        "logo": "🎬",
        "brand": "INOX",
        "facilities": ["Dolby Atmos", "INSIGNIA", "Luxury"],
        "color": "#0055a5"
    },
    {
        "id": "inox_banjara",
        "name": "INOX Banjara",
        "location": "Banjara Hills, Hyderabad",
        "logo": "🎬",
        "brand": "INOX",
        "facilities": ["4K Laser", "Dolby", "Bean Bag"],
        "color": "#0055a5"
    },
    {
        "id": "cinepolis_manjeera",
        "name": "Cinépolis",
        "location": "Manjeera Mall, Hyderabad",
        "logo": "🎥",
        "brand": "Cinépolis",
        "facilities": ["VIP Recliners", "4K", "Dolby Vision"],
        "color": "#e8871e"
    },
]

# ─── Food & Beverages Menu ───
FOOD_MENU = [
    # Popcorn
    {"id": "popcorn_salted_sm",  "name": "Salted Popcorn",     "size": "Small",  "category": "Popcorn",   "price": 120, "emoji": "🍿"},
    {"id": "popcorn_salted_lg",  "name": "Salted Popcorn",     "size": "Large",  "category": "Popcorn",   "price": 180, "emoji": "🍿"},
    {"id": "popcorn_caramel_sm", "name": "Caramel Popcorn",    "size": "Small",  "category": "Popcorn",   "price": 140, "emoji": "🍿"},
    {"id": "popcorn_caramel_lg", "name": "Caramel Popcorn",    "size": "Large",  "category": "Popcorn",   "price": 200, "emoji": "🍿"},
    {"id": "popcorn_cheese_sm",  "name": "Cheese Popcorn",     "size": "Small",  "category": "Popcorn",   "price": 150, "emoji": "🍿"},
    {"id": "popcorn_cheese_lg",  "name": "Cheese Popcorn",     "size": "Large",  "category": "Popcorn",   "price": 220, "emoji": "🍿"},
    # Cool Drinks
    {"id": "pepsi_sm",           "name": "Pepsi",              "size": "Medium", "category": "Drinks",    "price": 100, "emoji": "🥤"},
    {"id": "pepsi_lg",           "name": "Pepsi",              "size": "Large",  "category": "Drinks",    "price": 140, "emoji": "🥤"},
    {"id": "coke_sm",            "name": "Coca-Cola",          "size": "Medium", "category": "Drinks",    "price": 100, "emoji": "🥤"},
    {"id": "coke_lg",            "name": "Coca-Cola",          "size": "Large",  "category": "Drinks",    "price": 140, "emoji": "🥤"},
    {"id": "sprite_sm",          "name": "Sprite",             "size": "Medium", "category": "Drinks",    "price": 100, "emoji": "🥤"},
    {"id": "limca",              "name": "Limca",              "size": "Medium", "category": "Drinks",    "price": 90,  "emoji": "🥤"},
    {"id": "frooti",             "name": "Frooti Mango",       "size": "Medium", "category": "Drinks",    "price": 80,  "emoji": "🥭"},
    {"id": "water",              "name": "Mineral Water",      "size": "500ml",  "category": "Drinks",    "price": 40,  "emoji": "💧"},
    # Nachos & Snacks
    {"id": "nachos_salsa",       "name": "Nachos + Salsa",     "size": "Regular","category": "Snacks",    "price": 160, "emoji": "🌮"},
    {"id": "nachos_cheese",      "name": "Nachos + Cheese Dip","size": "Regular","category": "Snacks",    "price": 180, "emoji": "🌮"},
    {"id": "hotdog",             "name": "Hot Dog",            "size": "Regular","category": "Snacks",    "price": 140, "emoji": "🌭"},
    {"id": "burger",             "name": "Veg Burger",         "size": "Regular","category": "Snacks",    "price": 160, "emoji": "🍔"},
    # Combos
    {"id": "combo1",             "name": "Classic Combo",      "size": "1 Lg Popcorn + 2 Drinks", "category": "Combos", "price": 380, "emoji": "🎉"},
    {"id": "combo2",             "name": "Snack Combo",        "size": "Nachos + Popcorn + Drink", "category": "Combos", "price": 420, "emoji": "🎊"},
    {"id": "combo3",             "name": "Family Combo",       "size": "2 Popcorn + 4 Drinks",    "category": "Combos", "price": 650, "emoji": "👨‍👩‍👧‍👦"},
]


# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────

def get_movie_by_id(movie_id):
    """Find and return a movie dict by its ID."""
    for movie in MOVIES:
        if movie["id"] == int(movie_id):
            return movie
    return None

def get_booked_seats(movie_id, theatre_id, showtime):
    """Return the list of already-booked seats for a movie/theatre/showtime combo."""
    key = f"{movie_id}_{theatre_id}_{showtime.replace(' ', '_')}"
    return booked_seats.get(key, [])

def book_seats(movie_id, theatre_id, showtime, seats):
    """Save newly booked seats for a movie/theatre/showtime combo."""
    key = f"{movie_id}_{theatre_id}_{showtime.replace(' ', '_')}"
    existing = booked_seats.get(key, [])
    booked_seats[key] = existing + seats

def get_theatre_by_id(theatre_id):
    """Find and return a theatre dict by its ID."""
    for t in THEATRES:
        if t["id"] == theatre_id:
            return t
    return None

def calculate_food_total(food_items):
    """Calculate total cost of food items. food_items is list of (food_id, qty) tuples."""
    total = 0
    food_detail = []
    food_map = {f["id"]: f for f in FOOD_MENU}
    for item_id, qty in food_items:
        if item_id in food_map and qty > 0:
            food = food_map[item_id]
            subtotal = food["price"] * qty
            total += subtotal
            food_detail.append({
                "name": food["name"],
                "size": food["size"],
                "emoji": food["emoji"],
                "qty": qty,
                "price": food["price"],
                "subtotal": subtotal,
            })
    return total, food_detail


# ─────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────

@app.route("/")
def index():
    """Landing / splash page."""
    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """User registration page."""
    if request.method == "POST":
        name     = request.form.get("name", "").strip()
        email    = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm  = request.form.get("confirm_password", "")

        # Basic validation
        if not name or not email or not password:
            flash("All fields are required.", "error")
            return render_template("signup.html")

        if password != confirm:
            flash("Passwords do not match.", "error")
            return render_template("signup.html")

        if email in users:
            flash("An account with that email already exists.", "error")
            return render_template("signup.html")

        # Save the user (plain text password — use hashing in production!)
        users[email] = {"name": name, "email": email, "password": password}
        flash("Account created! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """User login page."""
    if request.method == "POST":
        email    = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = users.get(email)
        if user and user["password"] == password:
            # Store user info in session
            session["user_email"] = email
            session["user_name"]  = user["name"]
            flash(f"Welcome back, {user['name']}!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid email or password.", "error")

    return render_template("login.html")


@app.route("/logout")
def logout():
    """Clear session and redirect to landing page."""
    session.clear()
    flash("You've been logged out.", "info")
    return redirect(url_for("index"))


@app.route("/home")
def home():
    """Main movie listing page — requires login."""
    if "user_email" not in session:
        flash("Please log in to browse movies.", "error")
        return redirect(url_for("login"))
    return render_template("home.html", movies=MOVIES, user=session["user_name"])


@app.route("/tickets/<int:movie_id>", methods=["GET", "POST"])
def tickets(movie_id):
    """Seat selection page for a specific movie."""
    if "user_email" not in session:
        flash("Please log in to book tickets.", "error")
        return redirect(url_for("login"))

    movie = get_movie_by_id(movie_id)
    if not movie:
        flash("Movie not found.", "error")
        return redirect(url_for("home"))

    if request.method == "POST":
        showtime       = request.form.get("showtime")
        theatre_id     = request.form.get("theatre_id")
        selected_seats = request.form.getlist("seats")
        num_tickets    = len(selected_seats)

        # Validate required fields
        if not theatre_id:
            flash("Please select a theatre.", "error")
            already_booked = get_booked_seats(movie_id, theatre_id or THEATRES[0]["id"], showtime or movie["times"][0])
            return render_template("tickets.html", movie=movie, booked_seats=already_booked, theatres=THEATRES, food_menu=FOOD_MENU)

        if not showtime or not selected_seats:
            flash("Please select a showtime and at least one seat.", "error")
            already_booked = get_booked_seats(movie_id, theatre_id, showtime or movie["times"][0])
            return render_template("tickets.html", movie=movie, booked_seats=already_booked, theatres=THEATRES, food_menu=FOOD_MENU)

        # Check seat conflicts
        already_booked = get_booked_seats(movie_id, theatre_id, showtime)
        conflicts = [s for s in selected_seats if s in already_booked]
        if conflicts:
            flash(f"Seats {', '.join(conflicts)} were just taken. Please choose again.", "error")
            return render_template("tickets.html", movie=movie, booked_seats=already_booked, theatres=THEATRES, food_menu=FOOD_MENU)

        # Collect food orders: form sends food_qty_<item_id> for each item
        food_orders = []
        for food in FOOD_MENU:
            qty_str = request.form.get(f"food_qty_{food['id']}", "0")
            try:
                qty = int(qty_str)
            except ValueError:
                qty = 0
            if qty > 0:
                food_orders.append((food["id"], qty))

        food_total, food_detail = calculate_food_total(food_orders)

        # Save booking
        book_seats(movie_id, theatre_id, showtime, selected_seats)
        theatre = get_theatre_by_id(theatre_id)
        ticket_total = movie["price"] * num_tickets
        grand_total  = ticket_total + food_total

        session["booking"] = {
            "movie_title":   movie["title"],
            "movie_emoji":   movie["emoji"],
            "movie_poster":  movie["poster"],
            "showtime":      showtime,
            "seats":         selected_seats,
            "num_tickets":   num_tickets,
            "price_each":    movie["price"],
            "ticket_total":  ticket_total,
            "food_detail":   food_detail,
            "food_total":    food_total,
            "total_price":   grand_total,
            "theatre_name":  theatre["name"] if theatre else theatre_id,
            "theatre_loc":   theatre["location"] if theatre else "",
            "theatre_brand": theatre["brand"] if theatre else "",
            "user_name":     session["user_name"],
        }
        return redirect(url_for("confirmation"))

    # GET — show page with first showtime and first theatre
    initial_theatre  = request.args.get("theatre", THEATRES[0]["id"])
    initial_showtime = request.args.get("showtime", movie["times"][0])
    already_booked   = get_booked_seats(movie_id, initial_theatre, initial_showtime)
    return render_template("tickets.html", movie=movie, booked_seats=already_booked,
                           theatres=THEATRES, food_menu=FOOD_MENU)


@app.route("/confirmation")
def confirmation():
    """Booking confirmation page."""
    if "user_email" not in session:
        return redirect(url_for("login"))

    booking = session.get("booking")
    if not booking:
        flash("No active booking found.", "error")
        return redirect(url_for("home"))

    # Clear the booking from session after showing confirmation
    session.pop("booking", None)
    return render_template("tickets.html", booking=booking, confirmed=True)


@app.route("/about")
def about():
    """About page."""
    return render_template("about.html",
                           logged_in="user_email" in session,
                           user=session.get("user_name", ""))


@app.route("/contact", methods=["GET", "POST"])
def contact():
    """Contact page with a simple form."""
    if request.method == "POST":
        name    = request.form.get("name", "").strip()
        email   = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()
        if name and email and message:
            flash("Thanks for reaching out! We'll get back to you shortly.", "success")
        else:
            flash("Please fill in all fields.", "error")
        return redirect(url_for("contact"))

    return render_template("contact_us.html",
                           logged_in="user_email" in session,
                           user=session.get("user_name", ""))


# ─────────────────────────────────────────────
# AJAX ENDPOINT — fetch booked seats per showtime
# ─────────────────────────────────────────────

@app.route("/api/booked_seats")
def api_booked_seats():
    """Returns JSON list of booked seats for a given movie + theatre + showtime."""
    movie_id   = request.args.get("movie_id")
    theatre_id = request.args.get("theatre_id", THEATRES[0]["id"])
    showtime   = request.args.get("showtime", "")
    seats      = get_booked_seats(movie_id, theatre_id, showtime)
    return json.dumps({"booked": seats})


# ─────────────────────────────────────────────
# RUN THE APP
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("🎬 Movie Magic is starting...")
    print("   Visit: http://127.0.0.1:5000")
    app.run(debug=True)
