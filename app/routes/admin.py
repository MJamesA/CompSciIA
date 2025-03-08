from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import db, Admin, Student
from werkzeug.security import generate_password_hash, check_password_hash



admin_routes = Blueprint('admin_routes', __name__)

# User Type Selection
@admin_routes.route('/', methods=['GET', 'POST'])
def usertype():
    return render_template('UserTypeSelection.html')



# Admin Registration -- Temporary
@admin_routes.route('/admin/register', methods=['GET', 'POST'])
def admin_register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        password = request.form['password']

        if Admin.query.filter_by(Username=username).first():
            flash("Username already taken", "error")
            return redirect(url_for('admin_routes.admin_register'))

        admin = Admin(Firstname=first_name, Lastname=last_name, Username=username)
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()

        flash("Admin registered successfully", "success")
        return redirect(url_for('admin_routes.admin_login'))

    return render_template('admin/register.html')

# Admin Login
@admin_routes.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        admin = Admin.query.filter_by(Username=username).first()
        if admin and admin.check_password(password):
            session['user_type'] = 'admin'
            session['admin_id'] = admin.AdminID
            flash("Login successful", "success")
            return redirect(url_for('admin_routes.admin_homepage'))

        flash("Invalid username or password", "error")

    return render_template('admin/login.html')


# Temporary
@admin_routes.route('/temp', methods=['GET', 'POST'])
def temp():
    if 'user_type' not in session or session['user_type'] != 'admin':
        flash("You need to log in as an admin to access this page.", "error")
        return redirect(url_for('admin_routes.admin_login'))

    return render_template('/admin/formsubmission.html')

# Admin Homepage
@admin_routes.route('/admin/homepage')
def admin_homepage():
    if 'user_type' not in session or session['user_type'] != 'admin':
        flash("You need to log in as an admin to access this page.", "error")
        return redirect(url_for('admin_routes.admin_login'))

    admin = Admin.query.get(session['admin_id'])
    return render_template('admin/homepage.html', admin=admin)

# Admin Event Form
@admin_routes.route('/admin/eventform')
def eventform():
    if 'user_type' not in session or session['user_type'] != 'admin':
        flash("You need to log in as an admin to access this page.", "error")
        return redirect(url_for('admin_routes.admin_login'))

    return render_template('admin/eventform.html')

# Event Submission
@admin_routes.route('/admin/submission', methods=['GET', 'POST'])
def adminsubmission():
    if 'user_type' not in session or session['user_type'] != 'admin':
        flash("You need to log in as an admin to access this page.", "error")
        return redirect(url_for('admin_routes.admin_login'))

    return render_template('admin/eventsubmissiontemplate.html')

# Form Submitted
@admin_routes.route('/admin/formsub', methods=['GET', 'POST'])
def formsub():
    if 'user_type' not in session or session['user_type'] != 'admin':
        flash("You need to log in as an admin to access this page.", "error")
        return redirect(url_for('admin_routes.admin_login'))

    return render_template('/admin/formsubmission.html')

# Admin Calendar
@admin_routes.route('/admin/calendar')
def calendar():
    if 'user_type' not in session or session['user_type'] != 'admin':
        flash("You need to log in as an admin to access this page.", "error")
        return redirect(url_for('admin_routes.admin_login'))

    return render_template('admin/calendar.html') 

# Admin User Managment
@admin_routes.route('/admin/usermanagement')
def usermanagement():
    if 'user_type' not in session or session['user_type'] != 'admin':
        flash("You need to log in as an admin to access this page.", "error")
        return redirect(url_for('admin_routes.admin_login'))
        
    return render_template('admin/usermanagement.html')

# Admin Admins List
@admin_routes.route('/admin/user_list')
def admin_user_list():
    if 'user_type' not in session or session['user_type'] != 'admin':
        flash("You need to log in as an admin to access this page.", "error")
        return redirect(url_for('admin_routes.admin_login'))

    admin_users = Admin.query.all()
    return render_template('admin/admin_user_list.html', admin_users=admin_users)

# Admin Create Admin
@admin_routes.route('/admin/create_user', methods=['GET', 'POST'])
def create_admin_user():
    if 'user_type' not in session or session['user_type'] != 'admin':
        flash("You need to log in as an admin to access this page.", "error")
        return redirect(url_for('admin_routes.admin_login'))

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        password = request.form['password']

        existing_admin = Admin.query.filter_by(Username=username).first()
        if existing_admin:
            flash("Username already exists. Please choose a different one.", "error")
            return redirect(url_for('admin_routes.create_admin_user'))

        new_admin = Admin(Firstname=first_name, Lastname=last_name, Username=username)  
        new_admin.set_password(password)
        db.session.add(new_admin)
        db.session.commit()

        flash("Admin user created successfully!", "success")
        return redirect(url_for('admin_routes.admin_user_list'))  

    return render_template('admin/create_admin_user.html')

# Admin Profile (View and Update)
@admin_routes.route('/admin/profile/<int:admin_id>', methods=['GET', 'POST'])
def admin_profile(admin_id):
    if 'user_type' not in session or session['user_type'] != 'admin':
        flash("You need to log in as an admin to access this page.", "error")
        return redirect(url_for('admin_login'))

    admin = Admin.query.get(admin_id)

    if request.method == 'POST':
        admin.FirstName = request.form['first_name']
        admin.LastName = request.form['last_name']
        admin.Username = request.form['username']        

        if request.form['password']:
            admin.Password= generate_password_hash(request.form['password'])
        

        db.session.commit()
        flash("Profile updated successfully", "success")
        return redirect(url_for('admin_routes.admin_user_list'))

    return render_template('admin/admin_profile.html', admin=admin)

# Admin Delete User
@admin_routes.route('/admin/delete/<int:admin_id>', methods=['GET', 'POST'])
def admin_delete(admin_id):
    if 'user_type' not in session or session['user_type'] != 'admin':
        flash("You need to log in as an admin to access this page.", "error")
        return redirect(url_for('admin_login'))

    admin = Admin.query.get(admin_id)
    db.session.delete(admin)
    db.session.commit()

    return redirect(url_for('admin_routes.admin_user_list'))

# Admin Students list
@admin_routes.route('/admin/students')
def admin_students():
    if 'user_type' not in session or session['user_type'] != 'admin':
        flash("You need to log in as an admin to access this page.", "error")
        return redirect(url_for('admin_login'))

    students = Student.query.all()
    return render_template('admin/students_list.html', students=students)

# Admin add student
@admin_routes.route('/admin/add_student', methods=['GET', 'POST'])
def admin_add_student():
    if 'user_type' not in session or session['user_type'] != 'admin':
        flash("You need to log in as an admin to access this page.", "error")
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        id_card_number = request.form['id_card_number']

        if Student.query.filter_by(idcardnumber=id_card_number).first():
            flash("ID Card Number already exists", "error")
            return redirect(url_for('admin_routes.admin_add_student'))

        id_card_number = int(id_card_number)
        if Student.query.filter((id_card_number <= 100000) & (id_card_number >= 999999)).first():             
            flash("ID Card Number is not 6 Digits", "error")
            return redirect(url_for('admin_routes.admin_add_student'))

        student = Student(Firstname=first_name, Lastname=last_name, idcardnumber=id_card_number)
        db.session.add(student)
        db.session.commit()

        flash("Student added successfully", "success")
        return redirect(url_for('admin_routes.admin_students'))

    return render_template('admin/add_student.html')

# Admin view and update student 
@admin_routes.route('/admin/student/<int:student_id>', methods=['GET', 'POST'])
def admin_student_profile(student_id):
    if 'user_type' not in session or session['user_type'] != 'admin':
        flash("You need to log in as an admin to access this page.", "error")
        return redirect(url_for('admin_login'))

    student = Student.query.get_or_404(student_id)

    if request.method == 'POST':
        student.Firstname = request.form['first_name']
        student.Lastname = request.form['last_name']
        student.idcardnumber = request.form['id_card_number']

        id_card_number = int(request.form['id_card_number'])
        if id_card_number < 100000 or id_card_number > 999999:
            flash("ID Card Number must be exactly 6 digits", "error")
            return redirect(url_for('admin_routes.admin_add_student'))

        db.session.commit()
        flash("Student profile updated successfully", "success")
        return redirect(url_for('admin_routes.admin_students'))

    return render_template('admin/student_profile.html', student=student)

# Admin Delete Student
@admin_routes.route('/admin/studentdelete/<int:student_id>', methods=['GET', 'POST'])
def admin_student_delete(student_id):
    if 'user_type' not in session or session['user_type'] != 'admin':
        flash("You need to log in as an admin to access this page.", "error")
        return redirect(url_for('admin_login'))

    student = Student.query.get(student_id)
    db.session.delete(student)
    db.session.commit()

    return redirect(url_for('admin_routes.admin_students'))


# Admin Logout
@admin_routes.route('/admin/logout')
def admin_logout():
    session.clear()
    flash("Logged out successfully", "success")
    return redirect(url_for('admin_routes.admin_login'))
