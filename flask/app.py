# Flask Config
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'mysql+pymysql://user:password@db/mydatabase')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email

# Create all tables if they don't exists
with app.app_context():
    db.create_all()

# ******************************** Views **************************************
@app.route('/')
def hello():
    return "Hello World!"

@app.route('/view_users')
def view_users():
    users = User.query.all()
    all_users = []
    for user in users:
        all_users.append(user.email)
    return all_users


@app.route('/add_user/<id>')
def add_user(id):
    user = User("newUser" + id, "newUser+" + id + "@gmail.com")
    db.session.add(user)
    db.session.commit()
    return "User added..." + user.email

@app.route('/cache-me')
def cache():
    return "nginx will cache this response"

@app.route('/info')
def info():

    resp = {
        'host': request.headers['Host'],
        'user-agent': request.headers['User-Agent']
    }

    return jsonify(resp)

@app.route('/flask-health-check')
def flask_health_check():
    return "success"
