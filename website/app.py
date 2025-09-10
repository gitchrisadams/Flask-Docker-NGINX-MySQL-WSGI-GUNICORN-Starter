# Flask Config
from flask import Flask, request, jsonify, render_template
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'mysql+pymysql://user:password@db/mydatabase')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# *************************** Models ******************************************
class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, data, user_id):
        self.data = data
        self.user_id = user_id

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(1000))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')

    def __init__(self, email, password, first_name):
        self.email = email
        self.password = password
        self.first_name = first_name

# Create all tables if they don't exists
with app.app_context():
    db.create_all()

# ******************************** Views **************************************
@app.route('/')
def hello():
    myvar = "hello myvar"
    return render_template("index.html", myvar=myvar)

@app.route('/view_users')
def view_users():
    users = User.query.all()
    all_users = []
    for user in users:
        all_users.append([user.first_name, user.email, user.password])
    return all_users


@app.route('/add_user')
def add_user():
    user = User(email=request.args.get('email'), first_name=request.args.get('first_name'), password=request.args.get('password'))
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
