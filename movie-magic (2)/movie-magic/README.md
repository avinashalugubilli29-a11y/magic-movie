# 🎬 Movie Magic — Flask Ticket Booking App

A beginner-friendly movie ticket booking web application built with Python Flask.

---

## 📁 Project Structure

```
movie-magic/
├── app.py                    ← Flask backend (routes, logic, data)
├── requirements.txt          ← Python dependencies
├── templates/
│   ├── index.html            ← Landing / splash page
│   ├── login.html            ← User login
│   ├── signup.html           ← User registration
│   ├── home.html             ← Movie listings (requires login)
│   ├── tickets.html          ← Seat selection + booking confirmation
│   ├── about.html            ← About page
│   └── contact_us.html       ← Contact form
└── static/
    ├── css/
    │   └── style.css         ← All styling (dark cinematic theme)
    └── js/
        └── movies1.js        ← Genre filters, seat picker, AJAX
```

---

## 🚀 How to Run Locally

### Step 1 — Make sure Python is installed
```bash
python --version   # Should be Python 3.8+
```

### Step 2 — (Optional) Create a virtual environment
```bash
python -m venv venv

# Activate on macOS/Linux:
source venv/bin/activate

# Activate on Windows:
venv\Scripts\activate
```

### Step 3 — Install Flask
```bash
pip install -r requirements.txt
```

### Step 4 — Run the app
```bash
python app.py
```

### Step 5 — Open in your browser
```
http://127.0.0.1:5000
```

---

## 🎯 Features

| Feature | Description |
|---|---|
| **Sign Up / Log In** | Register and log in with email + password |
| **Movie Listings** | Browse 6 films with genre filter buttons |
| **Seat Selection** | Interactive 6×12 seat map with real-time availability |
| **Showtime Picker** | Switch showtimes and see updated booked seats via AJAX |
| **Booking Summary** | Live price calculation as you select seats |
| **Confirmation Page** | Styled ticket-style confirmation after booking |
| **About & Contact** | Informational pages with a working contact form |

---

## ⚠️ Important Notes for Beginners

1. **User data is in-memory** — all accounts and bookings reset when you restart the server.
   For a production app, you'd connect to a database (e.g. SQLite with Flask-SQLAlchemy).

2. **Passwords are stored in plain text** — in a real app, always hash passwords using
   `werkzeug.security.generate_password_hash`.

3. **No real payments** — prices are displayed for UI purposes only.

4. **`debug=True`** is enabled in `app.py` — turn this off in production.

---

## 🧩 Technologies Used

- **Python 3** + **Flask** — Backend framework
- **Jinja2** — HTML templating (built into Flask)
- **HTML5 / CSS3** — Markup and styling
- **Vanilla JavaScript** — No frameworks needed
- **Google Fonts** — Playfair Display + DM Sans

---

## 📸 Pages Overview

| URL | Page |
|---|---|
| `/` | Landing page |
| `/signup` | Registration |
| `/login` | Login |
| `/home` | Movie listings (auth required) |
| `/tickets/<id>` | Seat selection (auth required) |
| `/confirmation` | Booking confirmed |
| `/about` | About page |
| `/contact` | Contact form |
| `/api/booked_seats` | JSON API for seat availability |

---

Happy watching! 🍿
