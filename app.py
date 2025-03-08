# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from functools import wraps
import hashlib
from flask_migrate import Migrate
from app.models import db, Admin, Student, Event
from app.routes import init_routes
import os
from dotenv import load_dotenv
from flask_mail import Mail

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL') == 'True'
app.config['MAIL_USERNAME'] = "compsci2025ia@gmail.com"
app.config['MAIL_PASSWORD'] = "wdif rryv zfbd feto"
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

mysql = MySQL(app)
db.init_app(app)
migrate = Migrate(app, db)
mail = Mail(app)
# Create tables automatically if they don't exist
with app.app_context():
    db.create_all()
def create_tables():
    with app.app_context():
        db.create_all()
# Login decorator for admin routes
init_routes(app, db)

@app.route('/events')
def list_events():
    events = Event.query.all()  # Fetch all events from the database
    return render_template('events.html', events=events)

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)