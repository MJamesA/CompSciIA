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
        return f"<Student {self.FirstName} {self.LastName}>"