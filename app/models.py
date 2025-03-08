from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
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

    def set_password(self, password: str) -> None:
        
        self.Password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.Password, password)

    def __repr__(self):
        return f"<Admin {self.Username}>"
    

class Student(db.Model):
    __tablename__ = 'students'

    StudentID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Firstname = db.Column(db.String(20), nullable=False)
    Lastname = db.Column(db.String(20), nullable=False)
    idcardnumber = db.Column(db.Integer, nullable=False, unique=True)

   
    def __repr__(self):
        return f"<Student {self.Firstname} {self.Lastname}>"


class Event(db.Model):
    __tablename__ = 'EventsForm'

    EventID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    EventTitle = db.Column(db.String(255), nullable=False)
    Description = db.Column(db.Text, nullable=False)
    EmailAddress = db.Column(db.String(255), nullable=False)
    DateFilled = db.Column(db.DateTime, nullable=False)
    EventSupervisor = db.Column(db.String(255), nullable=False)
    SecurityStaff = db.Column(db.String(255), nullable=True)
    EventStart = db.Column(db.DateTime, nullable=False)
    EventEnd = db.Column(db.DateTime, nullable=False)
    # DateFilled = db.Column(db.DateTime, default=db.func.now())
    # organizer_name = db.Column(db.String(255), nullable=False)
    Location = db.Column(db.Text, nullable=True)
    Facilities = db.Column(db.Text, nullable=True)
    Resources = db.Column(db.Text, nullable=True)
    TeamMembers = db.Column(db.Text, nullable=True)
    ITResources = db.Column(db.Text, nullable=True)
    Finance = db.Column(db.String(255), nullable=True)
    Communications = db.Column(db.String(255), nullable=True)
    FirstAid = db.Column(db.String(255), nullable=True)
    NurseNote = db.Column(db.Text, nullable=True)
    Spectators = db.Column(db.String(255), nullable=False)
    EstSpectators = db.Column(db.Integer, nullable=False)
    Caretakers = db.Column(db.String(255), nullable=True)
    EventOrg = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Event {self.title}>"