from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Admin(db.Model):
    __tablename__ = 'admins'

    AdminID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Firstname = db.Column(db.String(20), nullable=False)
    Lastname = db.Column(db.String(20), nullable=False)
    Username = db.Column(db.String(50), nullable=False, unique=True)
    Password = db.Column(db.String(250), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    def set_password(self, password):
        """Hashes the password and stores it."""
        self.Password = generate_password_hash(password)

    def check_password(self, password):
        """Checks the password against the hashed version."""
        return check_password_hash(self.Password, password)

    def __repr__(self):
        return f"<Admin {self.Username}>"
    

class Student(db.Model):
    __tablename__ = 'students'

    StudentID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Firstname = db.Column(db.String(20), nullable=False)
    Lastname = db.Column(db.String(20), nullable=False)
    idcardnumber = db.Column(db.String(20), nullable=False, unique=True)

   
    def __repr__(self):
        return f"<Student {self.Firstname} {self.Lastname}>"


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    organizer_email = db.Column(db.String(255), nullable=False)
    event_date = db.Column(db.DateTime, nullable=False)
    supervisors = db.Column(db.String(255), nullable=False)
    security_staff = db.Column(db.String(255), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    date_filled = db.Column(db.DateTime, default=db.func.now())
    organizer_name = db.Column(db.String(255), nullable=False)
    location_facilities = db.Column(db.Text, nullable=True)
    resources_needed = db.Column(db.Text, nullable=True)
    team_members = db.Column(db.Text, nullable=True)
    it_resources = db.Column(db.Text, nullable=True)
    finance_department = db.Column(db.String(255), nullable=True)
    communication_department = db.Column(db.String(255), nullable=True)
    first_aid_required = db.Column(db.String(255), nullable=True)
    nurse_notes = db.Column(db.Text, nullable=True)
    spectators_count = db.Column(db.Integer, default=0)
    caretakers_count = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<Event {self.title}>"