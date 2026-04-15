from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import os
import razorpay

app = Flask(__name__)
app.secret_key = "secret123"
razorpay_client = razorpay.Client(auth=("rzp_test_SdNaLxEqcV4h3F", "9wXkQiAsLq3frFzimvZa9M7v"))
# ======================
# DATABASE
# ======================
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# ======================
# MODELS
# ======================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    movie = db.Column(db.String(100))
    show_time = db.Column(db.String(100))
    seats = db.Column(db.String(200))
class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    city = db.Column(db.String(50))
    theater = db.Column(db.String(100))
    time = db.Column(db.String(50))
    price = db.Column(db.String(20))

# ======================
# AUTO LOAD FUNCTION
# ======================
def load_data(folder):
    items = []
    path = f"static/images/{folder}"

    if not os.path.exists(path):
        return items

    for file in os.listdir(path):
        if file.endswith((".jpg", ".jpeg", ".png")):

            name = file.split(".")[0]
            title = name.replace("_", " ").title()

            item = {
                "title": title,
                "image": f"/static/images/{folder}/{file}"
            }

            # CATEGORY BASED DATA
            if folder == "movies":
                item.update({
                    "badge": "NEW",
                    "badge_color": "#f84464",
                    "rating": "8.5",
                    "votes": "(10k votes)",
                    "genre": "Entertainment",
                    "language": "EN",
                    "timings": ["10:00", "14:00", "18:00"]
                })

            elif folder == "plays":
                item.update({
                    "tag": "POPULAR",
                    "type": "Play",
                    "artist": title,
                    "date": "20 Apr",
                    "time": "7:00 PM",
                    "venue": "Pune",
                    "price": "₹500"
                })

            elif folder == "events":
                item.update({
                    "tag": "TRENDING",
                    "category": "Event",
                    "date": "25 Apr",
                    "venue": "Pune",
                    "price": "₹1000"
                })

            elif folder == "sports":
                item.update({
                    "tag": "LIVE",
                    "sport": "Match",
                    "date": "22 Apr",
                    "time": "7:30 PM",
                    "venue": "Stadium",
                    "price": "₹1500"
                })

            elif folder == "comedy":
                item.update({
                    "tag": "SELLING",
                    "comedian": title,
                    "show": "Standup",
                    "date": "18 Apr",
                    "time": "8:00 PM",
                    "venue": "Pune",
                    "price": "₹600"
                })

            items.append(item)

    return items

# ======================
# AUTH ROUTES
# ======================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(
            email=request.form['email'],
            password=request.form['password']
        ).first()

        if user:
            session['user_id'] = user.id
            return redirect('/')

    return render_template("login.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user = User(
            email=request.form['email'],
            password=request.form['password']
        )
        db.session.add(user)
        db.session.commit()
        return redirect('/login')

    return render_template("signup.html")


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# ======================
# HOME (AUTO LOAD)
# ======================
@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect('/login')

    return render_template(
        "index.html",
        movies=load_data("movies"),
        plays=load_data("plays"),
        events=load_data("events"),
        sports=load_data("sports"),
        comedy=load_data("comedy")
    )


@app.route('/host_login', methods=['GET', 'POST'])
def host_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email == "admin@gmail.com" and password == "admin123":
            session['host'] = True
            return redirect('/admin')

    return render_template("host_login.html")


# 👇 ADD THIS HERE
@app.route('/admin')
def admin():
    if not session.get('host'):
        return redirect('/host_login')

    shows = Show.query.all()
    return render_template("admin.html", shows=shows)
@app.route('/add_show', methods=['POST'])
def add_show():
    if not session.get('host'):
        return redirect('/host_login')

    new_show = Show(
        title=request.form['title'],
        city=request.form['city'],
        theater=request.form['theater'],
        time=request.form['time'],
        price=request.form['price']
    )

    db.session.add(new_show)
    db.session.commit()

    return redirect('/admin')

# ======================
# SHOWS (DUMMY FOR NOW)
# ======================
@app.route('/book/<title>')
def book(title):
    shows = [
        {"theater": "PVR Pune", "time": "10:00 AM", "seats": 50},
        {"theater": "INOX Mall", "time": "1:00 PM", "seats": 30},
        {"theater": "Cinepolis", "time": "6:00 PM", "seats": 10}
    ]

    return render_template("shows.html", movie=title, shows=shows)

# ======================
# SEATS
# ======================
@app.route('/seats/<title>/<time>')
def seats(title, time):
    return render_template("seats.html", movie=title, time=time)

# ======================
# CONFIRM → PAYMENT
# ======================
@app.route('/confirm', methods=['POST'])
def confirm():
    seats = request.form.getlist('seats')

    session['movie'] = request.form['movie']
    session['time'] = request.form['time']
    session['seats'] = ",".join(seats)

    return redirect('/payment')

# ======================
# PAYMENT
# ======================
@app.route('/payment', methods=['GET', 'POST'])
def payment():

    amount = 500 * 100  # ₹500 in paise

    order = razorpay_client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

    return render_template("payment.html", order=order)
@app.route('/payment_success', methods=['POST'])
def payment_success():

    data = request.get_json()

    payment_id = data.get('payment_id')
    order_id = data.get('order_id')
    signature = data.get('signature')

    try:
        razorpay_client.utility.verify_payment_signature({
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        })

        booking = Booking(
            user_id=session['user_id'],
            movie=session['movie'],
            show_time=session['time'],
            seats=session['seats']
        )

        db.session.add(booking)
        db.session.commit()

        return {"status": "success"}

    except:
        return {"status": "failed"}

# ======================
# DASHBOARD
# ======================
@app.route('/dashboard')
def dashboard():
    bookings = Booking.query.filter_by(user_id=session['user_id']).all()
    return render_template("dashboard.html", bookings=bookings)

# ======================
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)