from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import User, Course, Enrollment
from werkzeug.security import check_password_hash
from app import db

api = Blueprint('api', __name__)

@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity={'username': user.username, 'role': user.role})
        return jsonify({'access_token': access_token})
    return jsonify({'message': 'Invalid credentials'}), 401

@api.route('/courses', methods=['GET', 'POST'])
@jwt_required()
def handle_courses():
    current_user = get_jwt_identity()
    if request.method == 'POST':
        if current_user['role'] != 'admin':
            return jsonify({'message': 'Admin access required!'}), 403
        
        data = request.get_json()
        new_course = Course(
            coursename=data['coursename'],
            description=data['description']
        )
        db.session.add(new_course)
        db.session.commit()
        return jsonify({'message': 'Course created successfully!'})
    
    courses = Course.query.all()
    return jsonify([{'id': c.id, 'coursename': c.coursename, 'description': c.description} for c in courses])

@api.route('/courses/<int:course_id>/enroll', methods=['POST'])
@jwt_required()
def enroll(course_id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user['username']).first()
    course = Course.query.get(course_id)
    
    if not course:
        return jsonify({'message': 'Course not found'}), 404
    
    enrollment = Enrollment(user_id=user.id, course_id=course.id)
    db.session.add(enrollment)
    db.session.commit()
    
    return jsonify({'message': f'Enrolled in course {course.coursename} successfully!'})
