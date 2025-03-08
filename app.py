# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from functools import wraps
import hashlib
from flask_migrate import Migrate
from app.models import db, Admin, Student, Event
from app.routes import init_routes
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:malik168@localhost:3306/eventsform'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'

mysql = MySQL(app)
db.init_app(app)
migrate = Migrate(app, db)
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