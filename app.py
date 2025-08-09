from flask import Flask, render_template, request, redirect, url_for, session, send_file, flash
import sqlite3, os
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
from io import BytesIO
import qrcode

app = Flask(__name__)
app.secret_key = "haya_super_secret"
DB = "haya_ngizwe.db"
UPLOAD_FOLDER = os.path.join("static","uploads")
TICKETS_FOLDER = os.path.join("static","tickets")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TICKETS_FOLDER, exist_ok=True)

def init_db():
    with sqlite3.connect(DB) as c:
        cur = c.cursor()
        # Admin table
        cur.execute("CREATE TABLE IF NOT EXISTS admin (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)")
        # Welcome content
        cur.execute("CREATE TABLE IF NOT EXISTS welcome (id INTEGER PRIMARY KEY, language TEXT UNIQUE, message TEXT)")
        # About
        cur.execute("CREATE TABLE IF NOT EXISTS about (id INTEGER PRIMARY KEY, english TEXT, zulu TEXT, sesotho TEXT)")
        # Services
        cur.execute("CREATE TABLE IF NOT EXISTS services (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, description TEXT, language TEXT)")
        # Events
        cur.execute("CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, date TEXT, location TEXT, details TEXT, image_path TEXT, language TEXT)")
        # Gallery
        cur.execute("CREATE TABLE IF NOT EXISTS gallery (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, image_path TEXT, video_link TEXT, description TEXT, language TEXT)")
        # Blog
        cur.execute("CREATE TABLE IF NOT EXISTS blog (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT, image_path TEXT, post_date TEXT, language TEXT)")
        # Poetry registrations
        cur.execute("CREATE TABLE IF NOT EXISTS poetry_registration (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, phone TEXT, location TEXT, bio TEXT, language TEXT, submitted_at TEXT)")
        # Contact messages
        cur.execute("CREATE TABLE IF NOT EXISTS contact_messages (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, phone TEXT, message TEXT, submitted_at TEXT)")
        # Feedback
        cur.execute("CREATE TABLE IF NOT EXISTS feedback (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, location TEXT, rating INTEGER, comments TEXT, submitted_at TEXT)")
        # Market products
        cur.execute("CREATE TABLE IF NOT EXISTS market_products (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, category TEXT, description TEXT, price REAL, image_url TEXT, seller_name TEXT, seller_email TEXT, location TEXT, submitted_at TEXT)")
        # Donations
        cur.execute("CREATE TABLE IF NOT EXISTS donations (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, amount REAL, payment_method TEXT, message TEXT, submitted_at TEXT)")
        # Users
        cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT UNIQUE, password TEXT, bio TEXT, profile_pic TEXT, registered_at TEXT)")
        # Tickets
        cur.execute("CREATE TABLE IF NOT EXISTS tickets (id INTEGER PRIMARY KEY AUTOINCREMENT, event_title TEXT, buyer_name TEXT, buyer_email TEXT, seat TEXT, ticket_code TEXT, purchased_at TEXT)")
        c.commit()

def ensure_defaults():
    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM admin WHERE username='admin'")
        if not cur.fetchone():
            cur.execute("INSERT INTO admin (username, password) VALUES (?,?)", ('admin', generate_password_hash('admin123')))
        cur.execute("SELECT * FROM welcome WHERE language='en'")
        if not cur.fetchone():
            cur.execute("INSERT INTO welcome (language, message) VALUES (?,?)", ('en','Welcome to Haya Ngizwe Events!'))
        cur.execute("SELECT * FROM about WHERE id=1")
        if not cur.fetchone():
            cur.execute("INSERT INTO about (id, english, zulu, sesotho) VALUES (1,?,?,?)", ('Haya Ngizwe Events — art, poetry & community','Singabakwa Haya Ngizwe Events — ubuciko','Re Haya Ngizwe Events — bonono'))
        conn.commit()

@app.before_first_request
def setup():
    init_db()
    ensure_defaults()

# -- Routes (simplified and combined) --
@app.route('/')
def welcome():
    lang = request.args.get('lang','en')
    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        cur.execute("SELECT message FROM welcome WHERE language=?", (lang,))
        row = cur.fetchone()
        message = row[0] if row else "Welcome to Haya Ngizwe Events!"
    return render_template('welcome.html', content=message, lang=lang)

@app.route('/admin/login', methods=['GET','POST'])
def admin_login():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect(DB) as conn:
            cur = conn.cursor()
            cur.execute("SELECT password FROM admin WHERE username=?", (username,))
            row = cur.fetchone()
            if row and check_password_hash(row[0], password):
                session['admin'] = username
                return redirect(url_for('admin_dashboard'))
        flash("Invalid admin credentials","danger")
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    # show counts
    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM contact_messages"); contacts = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM poetry_registration"); regs = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM market_products"); products = cur.fetchone()[0]
    return render_template('dashboard.html', contacts=contacts, regs=regs, products=products)

# About
@app.route('/about')
def about():
    lang = request.args.get('lang','english')
    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        cur.execute("SELECT english, zulu, sesotho FROM about WHERE id=1")
        row = cur.fetchone()
    texts = {'english': row[0], 'zu': row[1], 'st': row[2]}
    content = texts.get(lang, row[0])
    return render_template('about.html', content=content)

# Services listing (simple)
@app.route('/services')
def services():
    lang = request.args.get('lang','en')
    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        cur.execute("SELECT title, description FROM services WHERE language=?", (lang,))
        items = cur.fetchall()
    return render_template('services.html', services=items)

# Events
@app.route('/events')
def events():
    lang = request.args.get('lang','en')
    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        cur.execute("SELECT title, date, location, details, image_path FROM events WHERE language=?", (lang,))
        items = cur.fetchall()
    return render_template('events.html', events=items)

# Gallery
@app.route('/gallery')
def gallery():
    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        cur.execute("SELECT title, image_path, video_link, description FROM gallery")
        items = cur.fetchall()
    return render_template('gallery.html', items=items)

# Blog
@app.route('/blog')
def blog():
    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        cur.execute("SELECT title, content, image_path, post_date FROM blog ORDER BY id DESC")
        posts = cur.fetchall()
    return render_template('blog.html', posts=posts)

# Poetry registration
@app.route('/poetry_slam', methods=['GET','POST'])
def poetry_slam():
    if request.method=='POST':
        name = request.form['name']; email = request.form['email']; phone = request.form['phone']
        location = request.form['location']; bio = request.form['bio']; language = request.form.get('language','en')
        submitted_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with sqlite3.connect(DB) as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO poetry_registration (name,email,phone,location,bio,language,submitted_at) VALUES (?,?,?,?,?,?,?)",
                        (name,email,phone,location,bio,language,submitted_at))
            conn.commit()
        return redirect(url_for('thank_you'))
    return render_template('poetry_slam.html')

# Contact
@app.route('/contact', methods=['GET','POST'])
def contact():
    if request.method=='POST':
        name = request.form['name']; email = request.form['email']; phone = request.form['phone']; message = request.form['message']
        submitted_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with sqlite3.connect(DB) as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO contact_messages (name,email,phone,message,submitted_at) VALUES (?,?,?,?,?)",
                        (name,email,phone,message,submitted_at))
            conn.commit()
        return redirect(url_for('thank_you'))
    return render_template('contact.html')

# Feedback
@app.route('/feedback', methods=['GET','POST'])
def feedback():
    if request.method=='POST':
        name = request.form['name']; email = request.form['email']; location = request.form.get('location','')
        rating = int(request.form.get('rating',5)); comments = request.form.get('comments','')
        submitted_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with sqlite3.connect(DB) as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO feedback (name,email,location,rating,comments,submitted_at) VALUES (?,?,?,?,?,?)",
                        (name,email,location,rating,comments,submitted_at))
            conn.commit()
        return redirect(url_for('thank_you'))
    return render_template('feedback.html')

# Market - product listing and upload
@app.route('/market', methods=['GET','POST'])
def market():
    if request.method=='POST':
        name = request.form['name']; category = request.form['category']; description = request.form['description']
        price = float(request.form.get('price','0') or 0); seller_name = request.form['seller_name']; seller_email = request.form['seller_email']; location = request.form.get('location','')
        image = request.files.get('image')
        img_url = ''
        if image:
            filename = secure_filename(image.filename)
            path = os.path.join(UPLOAD_FOLDER, filename)
            image.save(path)
            img_url = '/' + path.replace("\\","/")
        submitted_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with sqlite3.connect(DB) as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO market_products (name,category,description,price,image_url,seller_name,seller_email,location,submitted_at) VALUES (?,?,?,?,?,?,?,?,?)",
                        (name,category,description,price,img_url,seller_name,seller_email,location,submitted_at))
            conn.commit()
        return redirect(url_for('market'))
    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id,name,category,description,price,image_url FROM market_products ORDER BY id DESC")
        products = cur.fetchall()
    return render_template('market.html', products=products)

# Products & cart
@app.route('/products')
def products():
    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id,name,category,description,price,image_url FROM market_products")
        items = cur.fetchall()
    return render_template('products.html', items=items)

@app.route('/add_to_cart/<int:pid>', methods=['POST'])
def add_to_cart(pid):
    quantity = int(request.form.get('quantity',1))
    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id,name,price,image_url FROM market_products WHERE id=?", (pid,))
        p = cur.fetchone()
    if not p:
        flash("Product not found","danger"); return redirect(url_for('products'))
    cart = session.get('cart', {})
    key = str(pid)
    if key in cart:
        cart[key]['quantity'] += quantity
    else:
        cart[key] = {'id':p[0],'name':p[1],'price':float(p[2] or 0),'image_url':p[3],'quantity':quantity}
    session['cart'] = cart
    flash("Added to cart","success")
    return redirect(url_for('products'))

@app.route('/cart')
def cart():
    cart = session.get('cart', {})
    total = sum(item['price']*item['quantity'] for item in cart.values())
    return render_template('cart.html', cart=cart, total=total)

@app.route('/checkout', methods=['GET','POST'])
def checkout():
    if request.method=='POST':
        # placeholder for payment integration
        session.pop('cart', None)
        return redirect(url_for('thank_you'))
    cart = session.get('cart', {})
    total = sum(item['price']*item['quantity'] for item in cart.values())
    return render_template('checkout.html', cart=cart, total=total)

# Tickets
@app.route('/buy_ticket/<int:event_id>', methods=['GET','POST'])
def buy_ticket(event_id):
    if request.method=='POST':
        buyer_name = request.form['name']; buyer_email = request.form['email']; seat = request.form.get('seat','General')
        event_title = request.form.get('event_title', f'Event {event_id}')
        ticket_code = f"TKT-{event_id}-{int(datetime.now().timestamp())}"
        purchased_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with sqlite3.connect(DB) as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO tickets (event_title,buyer_name,buyer_email,seat,ticket_code,purchased_at) VALUES (?,?,?,?,?,?)",
                        (event_title,buyer_name,buyer_email,seat,ticket_code,purchased_at))
            conn.commit()
            tid = cur.lastrowid
        # generate qr
        qr = qrcode.make(ticket_code)
        path = os.path.join(TICKETS_FOLDER, f'ticket_{tid}.png')
        qr.save(path)
        return redirect(url_for('download_ticket', ticket_id=tid))
    return render_template('buy_ticket.html', event_id=event_id)

@app.route('/ticket/<int:ticket_id>/download')
def download_ticket(ticket_id):
    path = os.path.join(TICKETS_FOLDER, f'ticket_{ticket_id}.png')
    if not os.path.exists(path):
        return "Ticket not found", 404
    return send_file(path, as_attachment=True, download_name=f'ticket_{ticket_id}.png')

# Donations
@app.route('/donate', methods=['GET','POST'])
def donate():
    if request.method=='POST':
        name = request.form['name']; email = request.form['email']; amount = float(request.form.get('amount',0)); payment_method = request.form.get('payment_method','offline')
        message = request.form.get('message',''); submitted_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with sqlite3.connect(DB) as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO donations (name,email,amount,payment_method,message,submitted_at) VALUES (?,?,?,?,?,?)",
                        (name,email,amount,payment_method,message,submitted_at))
            conn.commit()
        return redirect(url_for('donation_thank_you'))
    return render_template('donate.html')

@app.route('/donation_thank_you')
def donation_thank_you():
    return render_template('donation_thank_you.html')

# Users (register/login/profile)
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        name = request.form['name']; email = request.form['email']; password = generate_password_hash(request.form['password'])
        bio = request.form.get('bio',''); registered_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            with sqlite3.connect(DB) as conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO users (name,email,password,bio,profile_pic,registered_at) VALUES (?,?,?,?,?,?)",
                            (name,email,password,bio,'',registered_at))
                conn.commit()
            flash('Registration successful, please login','success'); return redirect(url_for('user_login'))
        except Exception as e:
            flash('Error creating account: '+str(e),'danger')
    return render_template('register.html')

@app.route('/user/login', methods=['GET','POST'])
def user_login():
    if request.method=='POST':
        email = request.form['email']; password = request.form['password']
        with sqlite3.connect(DB) as conn:
            cur = conn.cursor()
            cur.execute("SELECT id,name,password FROM users WHERE email=?", (email,))
            row = cur.fetchone()
            if row and check_password_hash(row[2], password):
                session['user_id'] = row[0]; session['user_name']=row[1]
                flash('Logged in','success'); return redirect(url_for('profile'))
            flash('Invalid credentials','danger')
    return render_template('login.html')

@app.route('/profile', methods=['GET','POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('user_login'))
    uid = session['user_id']
    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id,name,email,bio,profile_pic FROM users WHERE id=?", (uid,))
        user = cur.fetchone()
    if request.method=='POST':
        name = request.form['name']; bio = request.form.get('bio','')
        with sqlite3.connect(DB) as conn:
            cur = conn.cursor()
            cur.execute("UPDATE users SET name=?, bio=? WHERE id=?", (name,bio,uid))
            conn.commit()
        flash('Profile updated','success'); return redirect(url_for('profile'))
    return render_template('profile.html', user=user)

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

if __name__=='__main__':
    setup()
    app.run(debug=True)
