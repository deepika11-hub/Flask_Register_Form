from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import re, os

app = Flask(__name__)
app.secret_key = 'super_secret_key_change_me'   

# ✅ MySQL Configuration (using environment variables)
app.config["MYSQL_HOST"] = os.getenv("MYSQLHOST", "centerbeam.proxy.rlwy.net")
app.config["MYSQL_USER"] = os.getenv("MYSQLUSER", "root")
app.config["MYSQL_PASSWORD"] = os.getenv("MYSQLPASSWORD", "ESSeXodulUKDndQKDvprSnuqQJGWEcQL")
app.config["MYSQL_DB"] = os.getenv("MYSQLDATABASE", "railway")
app.config["MYSQL_PORT"] = int(os.getenv("MYSQLPORT", 50326))
app.config["MYSQL_CURSORCLASS"] = 'DictCursor'

mysql = MySQL(app)
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return redirect(url_for('register'))  # ✅ only one home function

@app.route('/register', methods=['GET', 'POST'])
def register():
    # registration logic
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        mobile = request.form.get('mobile', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s OR email = %s OR mobile = %s',
    (username, email, mobile))


        if account:
            flash('Account already exists!', 'error')
        elif not username or not email or not password:
            flash('Please fill out all fields!', 'error')
        elif password != confirm_password:
            flash('Passwords do not match!', 'error')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!', 'error')
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash('Username must contain only letters and numbers!', 'error')
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            cursor.execute('INSERT INTO users (username, email, mobile, password) VALUES (%s, %s, %s, %s)',
    (username, email, mobile, hashed_password))

            mysql.connection.commit()
            flash('✅ Registration successful!', 'success')
            return redirect(url_for('register'))

        cursor.close()

    return render_template('register.html')

if __name__ == "__main__":
    app.run(debug=True)
