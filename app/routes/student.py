from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.models import db, Student, Event
from flask_mail import Mail, Message

# Initialize Flask-Mail
mail = Mail()


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

@student_routes.route('/events', methods=['GET', 'POST'])
def manage_events():
    if request.method == 'POST':
        # Extract form data
        new_event = Event(
            title=request.form['title'],
            description=request.form['description'],
            organizer_email=request.form['organizer_email'],
            event_date=request.form['event_date'],
            supervisors=request.form['supervisors'],
            security_staff=request.form['security_staff'],
            start_time=request.form['start_time'],
            end_time=request.form['end_time'],
            organizer_name=request.form['organizer_name'],
            location_facilities=request.form.get('location_facilities'),
            resources_needed=request.form.get('resources_needed'),
            team_members=request.form.get('team_members'),
            it_resources=request.form.get('it_resources'),
            finance_department=request.form.get('finance_department'),
            communication_department=request.form.get('communication_department'),
            first_aid_required=request.form.get('first_aid_required'),
            nurse_notes=request.form.get('nurse_notes')
        )
        # Save the event to the database
        db.session.add(new_event)
        db.session.commit()

        # Send email notification
        msg = Message('Event Created', sender='ia2025test@gmail.com', recipients=[new_event.organizer_email])
        msg.body = f"Your event '{new_event.title}' has been created successfully!"
        mail.send(msg)

        return jsonify({'message': 'Event created successfully! Email sent to organizer.'}), 201
    else:
        # Get all events for students
        events = Event.query.all()
        return jsonify([event.title for event in events])

@student_routes.route('/admin/events/<int:event_id>', methods=['GET', 'PUT', 'DELETE'])
def admin_event(event_id):
    event = Event.query.get_or_404(event_id)
    if request.method == 'GET':
        # Return event details for editing
        return jsonify({
            'title': event.title,
            'description': event.description,
            'organizer_email': event.organizer_email,
            'event_date': event.event_date,
            'supervisors': event.supervisors,
            'security_staff': event.security_staff,
            'start_time': event.start_time,
            'end_time': event.end_time,
            'organizer_name': event.organizer_name,
            'location_facilities': event.location_facilities,
            'resources_needed': event.resources_needed,
            'team_members': event.team_members,
            'it_resources': event.it_resources,
            'finance_department': event.finance_department,
            'communication_department': event.communication_department,
            'first_aid_required': event.first_aid_required,
            'nurse_notes': event.nurse_notes
        })
    elif request.method == 'PUT':
        data = request.get_json()
        event.title = data['title']
        event.description = data['description']
        event.organizer_email = data['organizer_email']
        event.event_date = data['event_date']
        event.supervisors = data['supervisors']
        event.security_staff = data['security_staff']
        event.start_time = data['start_time']
        event.end_time = data['end_time']
        event.organizer_name = data['organizer_name']
        event.location_facilities = data.get('location_facilities')
        event.resources_needed = data.get('resources_needed')
        event.team_members = data.get('team_members')
        event.it_resources = data.get('it_resources')
        event.finance_department = data.get('finance_department')
        event.communication_department = data.get('communication_department')
        event.first_aid_required = data.get('first_aid_required')
        event.nurse_notes = data.get('nurse_notes')
        db.session.commit()
        return jsonify({'message': 'Event updated successfully!'}), 200
    elif request.method == 'DELETE':
        db.session.delete(event)
        db.session.commit()
        return jsonify({'message': 'Event deleted successfully!'}), 204

@student_routes.route('/submit-event', methods=['GET'])
def submit_event():
    return render_template('admin/eventsubmissiontemplate.html')
