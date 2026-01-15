from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3, os, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = os.urandom(24)

# ---------- DATABASE PATH ----------
DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'bloodbank.db')
os.makedirs(os.path.join(os.path.dirname(__file__), 'data'), exist_ok=True)

# ---------- EMAIL CONFIG ----------
SENDER_EMAIL = "sangamevents80@gmail.com"
SENDER_PASSWORD = "lxlo ndtn jigl qrlr"  # App password

def send_email(to_email, subject, body):
    """Send email notification via Gmail SMTP"""
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        print(f"✅ Email sent to {to_email}")
    except Exception as e:
        print(f"❌ Email sending failed: {e}")

# ---------- DATABASE INIT ----------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS donors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        gender TEXT NOT NULL,
        blood_group TEXT NOT NULL,
        contact TEXT NOT NULL,
        location TEXT NOT NULL,
        approved INTEGER DEFAULT 0,
        email TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT NOT NULL,
        gender TEXT NOT NULL,
        blood_group TEXT NOT NULL,
        contact_info TEXT NOT NULL,
        location TEXT NOT NULL,
        approved INTEGER DEFAULT 0,
        email TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS hospital_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hospital_name TEXT NOT NULL,
        location TEXT NOT NULL,
        blood_group TEXT NOT NULL,
        contact_info TEXT NOT NULL,
        approved INTEGER DEFAULT 0,
        email TEXT NOT NULL
    )
    """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        notice_text TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)


    conn.commit()
    conn.close()

init_db()

# ---------- ROUTES ----------
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/index')
def index():
    return redirect(url_for('home'))

# ===== LOGIN & SIGNUP =====
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username, password = request.form['username'], request.form['password']

        # Admin Login
        if username == "admin" and password == "admin123":
            session['role'], session['username'] = 'admin', 'admin'
            return redirect(url_for('admin_dashboard'))

        # User Login
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['role'], session['username'] = 'user', username
            return redirect(url_for('user_dashboard'))
        else:
            flash("Invalid credentials!", "error")
    return render_template("login.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        phone = request.form['phone']

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password, email, phone) VALUES (?, ?, ?, ?)",
                           (username, password, email, phone))
            conn.commit()
            conn.close()
            flash("Account created successfully!", "success")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Username already exists!", "error")
    return render_template("signup.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ===== USER SECTION =====
@app.route('/user_dashboard')
def user_dashboard():
    if session.get('role') != 'user':
        return redirect(url_for('login'))

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT notice_text, created_at FROM notices ORDER BY created_at DESC LIMIT 1")
    notice = cursor.fetchone()
    conn.close()

    return render_template("user_dashboard.html", notice=notice)


@app.route('/donor_form', methods=['GET', 'POST'])
def donor_form():
    if session.get('role') != 'user':
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        blood_group = request.form['blood_group']
        contact = request.form['contact']
        location = request.form['location']

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT email FROM users WHERE username=?", (session['username'],))
        user_email = cursor.fetchone()[0]
        cursor.execute("INSERT INTO donors (name, gender, blood_group, contact, location, email) VALUES (?, ?, ?, ?, ?, ?)",
                       (name, gender, blood_group, contact, location, user_email))
        conn.commit()
        conn.close()

        flash("Donor registration submitted! Awaiting approval.", "info")
        return redirect(url_for('user_dashboard'))
    return render_template("donor_form.html")

# ===== BLOOD REQUEST TYPES =====
@app.route('/request_type')
def request_type():
    if session.get('role') != 'user':
        return redirect(url_for('login'))
    return render_template("request_type.html")

# ===== USER BLOOD REQUEST FORMS =====
@app.route('/request/patient', methods=['GET', 'POST'])
def patient_request_form():
    if session.get('role') != 'user':
        flash("Please login as user to access this page.", "error")
        return redirect(url_for('login'))

    if request.method == 'POST':
        patient_name = request.form['patient_name']
        gender = request.form['gender']
        blood_group = request.form['blood_group']
        location = request.form['location']
        hospital = request.form['hospital']
        contact_info = request.form['contact_info']

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT email FROM users WHERE username=?", (session['username'],))
        user_email = cursor.fetchone()[0]
        cursor.execute("""INSERT INTO requests (patient_name, gender, blood_group, contact_info, location, email)
                          VALUES (?, ?, ?, ?, ?, ?)""",
                       (patient_name, gender, blood_group, f"{hospital} | {contact_info}", location, user_email))
        conn.commit()
        conn.close()

        flash("Patient blood request submitted successfully!", "success")
        return redirect(url_for('user_dashboard'))

    return render_template("patient_request_form.html")


@app.route('/request/hospital', methods=['GET', 'POST'])
def hospital_request_form():
    if session.get('role') != 'user':
        flash("Please login as user to access this page.", "error")
        return redirect(url_for('login'))

    if request.method == 'POST':
        hospital_name = request.form['hospital_name']
        location = request.form['location']
        blood_group = request.form['blood_group']
        contact_info = request.form['contact_info']

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT email FROM users WHERE username=?", (session['username'],))
        user_email = cursor.fetchone()[0]
        cursor.execute("""INSERT INTO hospital_requests (hospital_name, location, blood_group, contact_info, email)
                          VALUES (?, ?, ?, ?, ?)""",
                       (hospital_name, location, blood_group, contact_info, user_email))
        conn.commit()
        conn.close()

        flash("Hospital blood request submitted successfully!", "success")
        return redirect(url_for('user_dashboard'))

    return render_template("hospital_request_form.html")


# ===== ADMIN SECTION =====
@app.route('/admin_dashboard')
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    return render_template("admin_dashboard.html")

@app.route('/admin_users')
def admin_users():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return render_template("users.html", users=users)

@app.route('/admin_donors')
def admin_donors():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM donors")
    donors = cursor.fetchall()
    conn.close()

    donors_by_group = {}
    for donor in donors:
        group = donor[3]
        donors_by_group.setdefault(group, []).append(donor)

    return render_template("donors.html", donors_by_group=donors_by_group)

@app.route('/admin_requests')
def admin_requests():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM requests")
    requests = cursor.fetchall()
    conn.close()
    return render_template("requests.html", requests=requests)

@app.route('/admin_hospital_requests')
def admin_hospital_requests():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM hospital_requests")
    requests = cursor.fetchall()
    conn.close()
    return render_template("hospital_requests.html", requests=requests)

@app.route('/admin_notices', methods=['GET', 'POST'])
def admin_notices():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if request.method == 'POST':
        notice_text = request.form['notice_text']
        
        # If a notice exists, update it; else insert
        cursor.execute("SELECT id FROM notices LIMIT 1")
        existing = cursor.fetchone()
        if existing:
            cursor.execute("UPDATE notices SET notice_text=? WHERE id=?", (notice_text, existing[0]))
        else:
            cursor.execute("INSERT INTO notices (notice_text) VALUES (?)", (notice_text,))
        conn.commit()
        flash("Notice updated successfully!", "success")
        return redirect(url_for('admin_notices'))

    cursor.execute("SELECT * FROM notices ORDER BY created_at DESC LIMIT 1")
    notice = cursor.fetchone()
    conn.close()

    return render_template("admin_notices.html", notice=notice)

# ===== APPROVAL =====
@app.route('/approve/<string:table>/<int:item_id>')
def approve_item(table, item_id):
    if session.get('role') != 'admin':
        return redirect(url_for('login'))

    if table not in ['donors', 'requests', 'hospital_requests']:
        flash("Invalid approval type!", "error")
        return redirect(url_for('admin_dashboard'))

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Approve the item
    cursor.execute(f"UPDATE {table} SET approved=1 WHERE id=?", (item_id,))
    
    # Fetch details for personalization
    if table == 'donors':
        cursor.execute("SELECT name, blood_group, location, contact, email FROM donors WHERE id=?", (item_id,))
        row = cursor.fetchone()
        name, blood_group, location, contact, email = row
    elif table == 'requests':
        cursor.execute("SELECT patient_name, blood_group, location, contact_info, email FROM requests WHERE id=?", (item_id,))
        row = cursor.fetchone()
        name, blood_group, location, contact, email = row
    elif table == 'hospital_requests':
        cursor.execute("SELECT hospital_name, blood_group, location, contact_info, email FROM hospital_requests WHERE id=?", (item_id,))
        row = cursor.fetchone()
        name, blood_group, location, contact, email = row

    conn.commit()
    conn.close()

    # Compose email
    subject = f"✅ {table[:-1].capitalize()} Approved - LifeLink Network"
    
    if table == "donors":
        body = (
            f"🎉 Dear {name},\n\n"
            "Your donor registration has been approved! 🩸\n"
            f"🩸 Blood Group: {blood_group}\n"
            f"📍 Location: {location}\n"
            f"📞 Contact: {contact}\n\n"
            "🙏 Thank you for joining LifeLink’s donor community and helping save lives!\n"
            "⏰ Our support team is available from 10 AM to 10 PM if you need any assistance.\n\n"
            "- 🌟 LifeLink Blood Network"
        )
    else:
        body = (
            f"✅ Dear {name},\n\n"
            "Your blood request has been approved! 🩸\n"
            f"🩸 Blood Group Needed: {blood_group}\n"
            f"📍 Location: {location}\n"
            f"📞 Contact Info: {contact}\n\n"
            "Our network of donors has been notified and will reach out to you soon. 💪\n"
            "⏰ For any queries or support, we are available from 10 AM to 10 PM.\n"
            "Stay strong and hopeful! 🌟\n\n"
            "- LifeLink Blood Network"
        )

    send_email(email, subject, body)
    flash(f"{table[:-1].capitalize()} approved successfully!", "success")
    return redirect(url_for(f"admin_{table}"))


# ===== DELETE =====
@app.route('/delete/<string:table>/<int:item_id>')
def delete_item(table, item_id):
    if session.get('role') != 'admin':
        return redirect(url_for('login'))

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table} WHERE id=?", (item_id,))
    conn.commit()
    conn.close()
    flash(f"{table[:-1].capitalize()} deleted successfully!", "success")
    return redirect(url_for(f"admin_{table}"))

# ===== MAIN RUN =====
if __name__ == "__main__":
    app.run(debug=True)
