from .admin import admin_routes
from .student import student_routes

def init_routes(app, db):
    # Registering the routes for admin and student
    app.register_blueprint(admin_routes)
    app.register_blueprint(student_routes)