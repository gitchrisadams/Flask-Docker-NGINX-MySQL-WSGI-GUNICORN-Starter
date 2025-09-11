# Flask Config
from flask import Flask, request, jsonify, render_template
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# MYSQL Database:
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'mysql+pymysql://user:password@db/mydatabase')

# Postgres Database:
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

# PostGres and MYSQL:
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SQL Lite Docker:
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////my/sqlite/path/sqlite.db'

# SQL Lite Local dev:
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///testdb.sqlite"

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
# Shows example of passing variable to a template
@app.route('/')
def hello():
    myvar = "hello myvar"
    return render_template("index.html", myvar=myvar)

# CREATE
@app.route('/add_user/<email>')
def add_user(email):
    user = User(email=email, first_name=request.args.get('first_name'), password=request.args.get('password'))
    db.session.add(user)
    db.session.commit()
    return "User added..." + user.email

# READ
@app.route('/view_users')
def view_users():
    users = User.query.all()
    all_users = []
    for user in users:
        all_users.append([user.first_name, user.email, user.password])
    return all_users

# UPDATE
@app.route('/update_by_email/<email>/<newemail>')
def update_by_email(email, newemail):
    user_to_update = User.query.filter_by(email=email).first()

    if user_to_update:
        user_to_update.email = newemail
        user_to_update.first_name = request.args.get("first_name")
        user_to_update.password = request.args.get("password")
        db.session.commit()
        return "User has been updated!"

# DELETE
@app.route('/delete_by_email/<email>')
def delete_user(email):
    user_to_delete = User.query.filter_by(email=email).first()
    if user_to_delete:
        db.session.delete(user_to_delete)
        db.session.commit()
        return "User Deleted"
    else:
        return "User Not Found"


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
