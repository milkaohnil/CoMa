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
    # (Gleiche Logik wie vorher)
