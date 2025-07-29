# app.py
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS # Import CORS
import uuid # For generating unique IDs for cart items and bookings
import os
import hashlib # For password hashing
import secrets # For session key

app = Flask(__name__)
# Generate a strong, random secret key for session management.
# In a production environment, this should be loaded from an environment variable.
app.secret_key = secrets.token_hex(16)

# Enable CORS for all origins on all routes.
# In a production environment, you should restrict origins to your frontend's domain.
CORS(app)

# --- In-memory Data Stores (for simplicity, data resets on server restart) ---
# Users: {user_id: {username, password_hash}}
users = {}
# Treks: {trek_id: {name, location, price, description, image_url, offers}}
treks = {
    "trek-1": {
        "name": "Everest Base Camp Trek",
        "location": "Nepal Himalayas",
        "price": 1500,
        "description": "An iconic journey to the base of the world's highest peak, offering breathtaking views and cultural immersion.",
        "image_url": "https://placehold.co/600x400/007bff/ffffff?text=Everest+Trek",
        "offers": ["10% off for early bird", "Free local guide"]
    },
    "trek-2": {
        "name": "Annapurna Circuit Trek",
        "location": "Nepal",
        "price": 1200,
        "description": "A classic trek around the Annapurna massif, known for its diverse landscapes and rich culture.",
        "image_url": "https://placehold.co/600x400/28a745/ffffff?text=Annapurna+Trek",
        "offers": ["Group discount available"]
    },
    "trek-3": {
        "name": "Roopkund Lake Trek",
        "location": "Uttarakhand, India",
        "price": 700,
        "description": "A mysterious high-altitude glacial lake trek, famous for skeletal remains found at its bottom.",
        "image_url": "https://placehold.co/600x400/dc3545/ffffff?text=Roopkund+Trek",
        "offers": []
    },
    "trek-4": {
        "name": "Valley of Flowers Trek",
        "location": "Uttarakhand, India",
        "price": 550,
        "description": "A vibrant and picturesque trek through a UNESCO World Heritage Site, blooming with endemic alpine flowers.",
        "image_url": "https://placehold.co/600x400/ffc107/000000?text=Valley+of+Flowers",
        "offers": ["Seasonal discount"]
    }
}
# Carts: {user_id: {cart_item_id: {trek_id, quantity}}}
# For unauthenticated users, cart will be stored in session directly.
# Bookings: {booking_id: {user_id, items: [{trek_id, quantity, price}], total_amount, status}}
bookings = {}

# --- Helper Functions ---
def hash_password(password):
    """Hashes a password using SHA256."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def check_password(hashed_password, user_password):
    """Checks if a given password matches the hashed password."""
    return hashed_password == hashlib.sha256(user_password.encode('utf-8')).hexdigest()

# --- Routes for serving HTML pages ---

@app.route('/')
def home():
    """Renders the home page."""
    # Pass the entire treks dictionary so that index.html can iterate using .items()
    return render_template('index.html', treks=treks)

@app.route('/treks')
def treks_page():
    """Renders the treks listing page."""
    # Pass the entire treks dictionary so that treks.html can iterate using .items()
    return render_template('treks.html', treks=treks)

@app.route('/trek/<trek_id>')
def trek_detail_page(trek_id):
    """Renders the detailed page for a specific trek."""
    trek = treks.get(trek_id)
    if not trek:
        return render_template('404.html'), 404 # Or redirect to treks page with an error
    return render_template('trek_detail.html', trek=trek, trek_id=trek_id)

@app.route('/cart')
def cart_page():
    """Renders the cart page."""
    return render_template('cart.html')

@app.route('/booking')
def booking_page():
    """Renders the booking page."""
    return render_template('booking.html')

@app.route('/offers')
def offers_page():
    """Renders the offers page."""
    # Filter treks that have offers
    treks_with_offers = [t for t in treks.values() if t.get('offers')]
    return render_template('offers.html', treks=treks_with_offers)

@app.route('/about')
def about_page():
    """Renders the about us page."""
    return render_template('about.html')

@app.route('/contact')
def contact_page():
    """Renders the contact us page."""
    return render_template('contact.html')

@app.route('/login')
def login_page():
    """Renders the login page."""
    return render_template('login.html')

@app.route('/register')
def register_page():
    """Renders the registration page."""
    return render_template('register.html')

# --- API Endpoints ---

@app.route('/api/register', methods=['POST'])
def register_user():
    """API endpoint for user registration."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    if username in [u['username'] for u in users.values()]:
        return jsonify({"message": "Username already exists"}), 409

    user_id = str(uuid.uuid4())
    users[user_id] = {
        "username": username,
        "password_hash": hash_password(password)
    }
    return jsonify({"message": "User registered successfully", "user_id": user_id}), 201

@app.route('/api/login', methods=['POST'])
def login_user():
    """API endpoint for user login."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    user_found = False
    for user_id, user_data in users.items():
        if user_data['username'] == username and check_password(user_data['password_hash'], password):
            session['user_id'] = user_id
            session['username'] = username
            user_found = True
            break

    if user_found:
        return jsonify({"message": "Login successful", "username": username}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401

@app.route('/api/logout', methods=['POST'])
def logout_user():
    """API endpoint for user logout."""
    session.pop('user_id', None)
    session.pop('username', None)
    return jsonify({"message": "Logged out successfully"}), 200

@app.route('/api/treks', methods=['GET'])
def get_treks():
    """API endpoint to get all treks."""
    return jsonify([{"id": k, **v} for k, v in treks.items()]), 200

@app.route('/api/treks/<trek_id>', methods=['GET'])
def get_trek_detail(trek_id):
    """API endpoint to get details of a specific trek."""
    trek = treks.get(trek_id)
    if trek:
        return jsonify({"id": trek_id, **trek}), 200
    else:
        return jsonify({"message": "Trek not found"}), 404

@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    """API endpoint to add a trek to the cart."""
    data = request.get_json()
    trek_id = data.get('trek_id')
    quantity = int(data.get('quantity', 1))

    if not trek_id or trek_id not in treks:
        return jsonify({"message": "Invalid trek ID"}), 400
    if quantity <= 0:
        return jsonify({"message": "Quantity must be positive"}), 400

    # Initialize cart in session if it doesn't exist
    if 'cart' not in session:
        session['cart'] = {}

    # Add/update item in cart
    if trek_id in session['cart']:
        session['cart'][trek_id]['quantity'] += quantity
    else:
        session['cart'][trek_id] = {
            "trek_id": trek_id,
            "quantity": quantity,
            "name": treks[trek_id]['name'],
            "price": treks[trek_id]['price'],
            "image_url": treks[trek_id]['image_url']
        }
    session.modified = True # Mark session as modified to ensure it's saved

    return jsonify({"message": "Item added to cart", "cart": session['cart']}), 200

@app.route('/api/cart/update', methods=['POST'])
def update_cart():
    """API endpoint to update quantity of a trek in the cart."""
    data = request.get_json()
    trek_id = data.get('trek_id')
    quantity = int(data.get('quantity', 0))

    if 'cart' not in session or trek_id not in session['cart']:
        return jsonify({"message": "Item not in cart"}), 404

    if quantity <= 0:
        # Remove item if quantity is 0 or less
        del session['cart'][trek_id]
    else:
        session['cart'][trek_id]['quantity'] = quantity
    session.modified = True

    return jsonify({"message": "Cart updated", "cart": session['cart']}), 200

@app.route('/api/cart/remove', methods=['POST'])
def remove_from_cart():
    """API endpoint to remove a trek from the cart."""
    data = request.get_json()
    trek_id = data.get('trek_id')

    if 'cart' not in session or trek_id not in session['cart']:
        return jsonify({"message": "Item not in cart"}), 404

    del session['cart'][trek_id]
    session.modified = True

    return jsonify({"message": "Item removed from cart", "cart": session['cart']}), 200

@app.route('/api/cart', methods=['GET'])
def get_cart():
    """API endpoint to get current cart contents."""
    cart_items = []
    total_price = 0
    if 'cart' in session:
        for trek_id, item_data in session['cart'].items():
            trek_info = treks.get(trek_id)
            if trek_info:
                item_price = trek_info['price'] * item_data['quantity']
                cart_items.append({
                    "trek_id": trek_id,
                    "name": trek_info['name'],
                    "price": trek_info['price'],
                    "quantity": item_data['quantity'],
                    "total_item_price": item_price,
                    "image_url": trek_info['image_url']
                })
                total_price += item_price
    return jsonify({"cart_items": cart_items, "total_price": total_price}), 200

@app.route('/api/book', methods=['POST'])
def book_trek():
    """API endpoint to process a booking."""
    if 'cart' not in session or not session['cart']:
        return jsonify({"message": "Cart is empty, cannot book"}), 400

    user_id = session.get('user_id', 'guest') # Associate with user if logged in, else guest
    cart_items_for_booking = []
    total_amount = 0

    for trek_id, item_data in session['cart'].items():
        trek_info = treks.get(trek_id)
        if trek_info:
            item_total = trek_info['price'] * item_data['quantity']
            cart_items_for_booking.append({
                "trek_id": trek_id,
                "name": trek_info['name'],
                "quantity": item_data['quantity'],
                "price_per_unit": trek_info['price'],
                "total_item_price": item_total
            })
            total_amount += item_total

    booking_id = str(uuid.uuid4())
    bookings[booking_id] = {
        "user_id": user_id,
        "items": cart_items_for_booking,
        "total_amount": total_amount,
        "status": "confirmed",
        "booking_date": "2025-07-29" # Static date for simplicity
    }

    # Clear the cart after booking
    session.pop('cart', None)
    session.modified = True

    return jsonify({"message": "Booking successful", "booking_id": booking_id, "booking_details": bookings[booking_id]}), 201

# --- User Session Check ---
@app.route('/api/user_status', methods=['GET'])
def get_user_status():
    """API endpoint to check user login status."""
    if 'user_id' in session:
        return jsonify({"logged_in": True, "username": session['username']}), 200
    else:
        return jsonify({"logged_in": False}), 200

if __name__ == '__main__':
    # Create a 'templates' directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    # Create a 'static' directory if it doesn't exist
    if not os.path.exists('static'):
        os.makedirs('static')

    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
