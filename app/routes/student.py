from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import db, Student

student_routes = Blueprint('student_routes', __name__)

# Student Registration
@student_routes.route('/student/register', methods=['GET', 'POST'])
def student_register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        id_card = request.form['id_card']
        password = request.form['password']

        # Check if IDCardNumber already exists
        if Student.query.filter_by(IDCardNumber=id_card).first():
            flash("ID Card Number already registered", "error")
            return redirect(url_for('student_register'))

        # Create and save the new student
        student = Student(FirstName=first_name, LastName=last_name, IDCardNumber=id_card)
        student.set_password(password)
        db.session.add(student)
        db.session.commit()

        flash("Student registered successfully", "success")
        return redirect(url_for('student_login'))

    return render_template('student/register.html')


# Student Login
@student_routes.route('/student/login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        id_card = request.form['id_card']
        lastname = request.form['name']


        student = Student.query.filter_by(idcardnumber=id_card).first()
        if student.idcardnumber == id_card and student.Lastname == lastname:
            session['user_type'] = 'student'
            session['student_id'] = student.StudentID
            flash("Login successful", "success")
            return redirect(url_for('student_routes.student_homepage'))

        flash("Invalid ID card or password", "error")

    return render_template('student/login.html')


# Student Dashboard
@student_routes.route('/student/homepage', methods=['GET', 'POST'])
def student_homepage():
    if 'user_type' not in session or session['user_type'] != 'student':
        flash("You need to log in as a student to access this page.", "error")
        return redirect(url_for('student_login'))

    student = Student.query.get(session['student_id'])
    return render_template('student/homepage.html', student=student)

@student_routes.route('/student/eventform', methods=['GET', 'POST'])
def eventform():
    if 'user_type' not in session or session['user_type'] != 'student':
        flash("You need to log in as a student to access this page.", "error")
        return redirect(url_for('student_login'))

    student = Student.query.get(session['student_id'])
    return render_template('student/eventform.html') 

@student_routes.route('/student/calendar', methods=['GET', 'POST'])
def calendar():
    if 'user_type' not in session or session['user_type'] != 'student':
        flash("You need to log in as a student to access this page.", "error")
        return redirect(url_for('student_login'))

    student = Student.query.get(session['student_id'])
    return render_template('student/calendar.html') 

# Student Profile (View and Update)
@student_routes.route('/student/profile', methods=['GET', 'POST'])
def student_profile():
    if 'user_type' not in session or session['user_type'] != 'student':
        flash("You need to log in as a student to access this page.", "error")
        return redirect(url_for('student_login'))

    student = Student.query.get(session['student_id'])

    if request.method == 'POST':
        student.FirstName = request.form['first_name']
        student.LastName = request.form['last_name']

        db.session.commit()
        flash("Profile updated successfully", "success")
        return redirect(url_for('student_profile'))

    return render_template('student/profile.html', student=student)


# Student Logout
@student_routes.route('/student/logout')
def student_logout():
    session.clear()
    flash("Logged out successfully", "success")
    return redirect(url_for('student_login'))
