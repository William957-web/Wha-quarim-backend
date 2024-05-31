from flask import Flask, render_template, request, redirect, url_for, session, g
from hashlib import sha256
import sqlite3
import json
import os

app = Flask(__name__)
app.secret_key = b'Whaleeethinkingthinking'
key=b'Wha!Quar1uM_is_s3cureeeee_ssseecretttttt'

DATABASE = 'blog.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username=='admin' and sha256(password.encode()).hexdigest()=='0cfbb54e47d8b2bc37a13791296747649ed7b1611d5d7bc85192a4c00e2dab84':
            session['username'] = username
            return redirect('admin')
        else:
            return render_template('login.html', msg='Invalid username or password.')
    return render_template('login.html')

@app.route('/admin', methods=['GET'])
def admin():
    if not session or not session['username']:
        return render_template('login.html', msg="Login First")
    else:
        return render_template('admin.html')

@app.route('/admin-food', methods=['GET', 'POST'])
def admin_food():
    if not session or not session['username']:
        return redirect('admin-login')
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        power = request.form['power']
        db = get_db()
        cur = db.execute("INSERT INTO food (name, price, power) VALUES (?, ?, ?);", (name, price, power))
        db.commit()
        return redirect('admin-food')
    else:
        db = get_db()
        cur = db.execute('SELECT * FROM food ORDER BY id DESC')
        foods = cur.fetchall()
        return render_template('admin_food.html', foods=foods)

@app.route('/admin-fish', methods=['GET', 'POST'])
def admin_fish():
    if not session or not session['username']:
        return redirect('admin-login')
    db = get_db()
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        hunger = request.form['hunger']
        length = request.form['length']
        food_time = request.form['food_time']
        cur = db.execute("INSERT INTO fish (name, price, hunger, long, food_time) VALUES (?, ?, ?, ?, ?);", (name, price, hunger, length, food_time))
        db.commit() 
        return redirect('admin-fish')
    cur = db.execute("SELECT * FROM fish ORDER BY id DESC")
    fishes = cur.fetchall()
    data={}
    data['fishes']=fishes
    print(json.dumps(data, default=list), type(data))
    return render_template('admin_fish.html', fishes=fishes)

@app.route('/admin-sql', methods=['GET', 'POST'])
def admin_sql():
    if not session or not session['username']:
        return redirect('admin-login')
    db = get_db()
    if request.method == 'POST':
        sql = request.form['sql']
        cur = db.execute(sql)
        db.commit() 
        return redirect('admin-sql')
    return render_template('admin_sql.html')

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username')
    return redirect('admin-login')
    
@app.route('/api/reg/username/<username>/password/<pwd>')
def reg(username, pwd):
    db = get_db()
    cur = db.execute('SELECT * FROM users WHERE username=?', (username,))
    cur=cur.fetchall()
    if cur:
        return "Username already been used"
    else:
        token=sha256(username.encode()+os.urandom(16)).hexdigest()
        cur = db.execute("INSERT INTO users (username, password, fishes, foods, money, play, pre_fishes, achieve, token) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);", (username, sha256(pwd.encode()).hexdigest(), '{}', '{}', 100, 0, '{}', '{}', token))
        db.commit() 
        return token

@app.route('/api/login/username/<username>/password/<pwd>')
def login(username, pwd):
    db = get_db()
    cur = db.execute('SELECT token FROM users WHERE username=? AND password=?', (username, sha256(pwd.encode()).hexdigest(),))
    cur=cur.fetchone()
    if cur:
        return cur['token']
    else:
        return "Wrong password or username"

@app.route('/api/getUserdata/token/<token>')
def getUserdata(token):
    db = get_db()
    cur = db.execute('SELECT * FROM users WHERE token=?', (token,))
    datas = cur.fetchall()
    data={}
    data['userdata']=datas
    print(json.dumps(data, default=list), type(data), type(json.dumps(data, default=list)))
    return json.dumps(data, default=list)

@app.route('/api/userlogout/<token>')
def userlogout(token):
    db = get_db()
    cur = db.execute('UPDATE users SET token=? WHERE token=?', (sha256(token.encode()+os.urandom(16)).hexdigest(), token,))
    db.commit()
    return 'logout success'

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=80)
