from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.models import db, Student, Event
from flask_mail import Mail, Message

mail = Mail()


student_routes = Blueprint('student_routes', __name__)

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

# Student Homepage
@student_routes.route('/student/homepage', methods=['GET', 'POST'])
def student_homepage():
    if 'user_type' not in session or session['user_type'] != 'student':
        flash("You need to log in as a student to access this page.", "error")
        return redirect(url_for('student_login'))

    student = Student.query.get(session['student_id'])
    return render_template('student/homepage.html', student=student)

# Student Event Form
@student_routes.route('/student/eventform', methods=['GET', 'POST'])
def eventform():
    if 'user_type' not in session or session['user_type'] != 'student':
        flash("You need to log in as a student to access this page.", "error")
        return redirect(url_for('student_login'))

    student = Student.query.get(session['student_id'])
    return render_template('student/eventform.html') 

# Student Calendar
@student_routes.route('/student/calendar', methods=['GET', 'POST'])
def calendar():
    if 'user_type' not in session or session['user_type'] != 'student':
        flash("You need to log in as a student to access this page.", "error")
        return redirect(url_for('student_routes.student_login'))

    submitted_forms = db.session.query(Event).filter_by(Status="Officialized").all()
    return render_template('student/calendarlist.html', submitted_forms=submitted_forms) 

# View a Calendar Entry
@student_routes.route('/student/viewcalendar/<int:EventID>', methods=['GET', 'POST'])
def viewcalendar(EventID):
    if 'user_type' not in session or session['user_type'] != 'student':
        flash("You need to log in as a student to access this page.", "error")
        return redirect(url_for('student_login'))

    submitted_form = Event.query.get(EventID)

    return render_template('student/calendarview.html', submitted_form=submitted_form )

# Student Logout
@student_routes.route('/student/logout')
def student_logout():
    session.clear()
    flash("Logged out successfully", "success")
    return redirect(url_for('student_login'))

# Event form submission emails and database push
@student_routes.route('/events', methods=['GET', 'POST'])
def manage_events():
    if request.method == 'POST':
        new_event = Event(
            EventTitle=request.form['title'],
            Description=request.form['description'],
            EmailAddress=request.form['organizer_email'],
            DateFilled=request.form['event_date'],
            EventSupervisor=request.form['supervisors'],
            SecurityStaff=request.form['security_staff'],
            EventStart=request.form['start_time'],
            EventEnd=request.form['end_time'],
            Location=request.form.get('location'),
            Facilities=request.form.get('facilities'),
            Resources=request.form.get('resources_needed'),
            TeamMembers=request.form.get('team_members'),
            Spectators=request.form.get('participants'),
            EstSpectators=request.form.get('estspectators'),
            ITResources=request.form.get('it_resources'),
            Finance=request.form.get('finance_department'),
            Communications=request.form.get('communication_department'),
            FirstAid=request.form.get('first_aid_required'),
            NurseNote=request.form.get('nurse_notes'),
            Caretakers=request.form.get('caretakers'),
            EventOrg=request.form.get('event_organiser'),
            Status="SUBMITTED"
        )
        db.session.add(new_event)
        db.session.commit()

        msg = Message('Event Created', sender=' ia2025test@gmail.com', recipients=[new_event.EmailAddress])
        msg.body = f"Your event '{new_event.EventTitle}' has been created successfully!"
        mail.send(msg)

        HOSapprove = url_for('admin_routes.HOSapproval', EventID=new_event.EventID, _external=True)

        msg = Message('Event Created', sender=' ia2025test@gmail.com', recipients=["compsci2025ia+HOS@gmail.com"])
        msg.body = f"An event, '{new_event.EventTitle}' has been submitted by '{new_event.EventOrg}'! \n\nTo review the Event form please follow this link: {HOSapprove}"
        mail.send(msg)

        return jsonify({'message': 'Event created successfully! Email sent to organizer and HOS.'}), 201
    
    else:
        events = Event.query.all()
        return jsonify([event.EventTitle for event in events])

# Student Event Submission
@student_routes.route('/student/submission', methods=['GET', 'POST'])
def studentsubmission():
    if 'user_type' not in session or session['user_type'] != 'student':
        flash("You need to log in as a student to access this page.", "error")
        return redirect(url_for('student_login'))

    return render_template('student/eventsubmissiontemplate.html')


@student_routes.route('/submit-event', methods=['GET'])
def submit_event():
    return render_template('admin/eventsubmissiontemplate.html')

@student_routes.route('/testemail', methods=['GET'])
def testemail():
        msg = Message('Event Created', sender=' ia2025test@gmail.com', recipients=[""])
        msg.body = f"Your event 'testing' has been created successfully!"
        mail.send(msg)

        return jsonify({'message': 'Event created successfully! Email sent to organizer.'}), 201