from flask import Blueprint, request
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from flasgger import swag_from
from datetime import datetime, timedelta

from .extensions import db
from .models import User


auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


@auth.post('/register')
@swag_from('./docs/register.yaml')
def register():
    username = request.json['username']
    password = request.json['password']

    user = User.query.filter_by(username=username).first()

    if user:
        return {'success': False, 'reason': 'Username has been used.'}, 409

    if len(username) < 3:
        return {'success': False, 'reason': 'Username is too short.'}, 400

    if len(username) > 32:
        return {'success': False, 'reason': 'Username is too long.'}, 400

    if len(password) < 8:
        return {'success': False, 'reason': 'Password is too short.'}, 400

    if len(password) > 32:
        return {'success': False, 'reason': 'Password is too long.'}, 400

    if password.isdigit():
        return {'success': False, 'reason': 'Password should contain at least 1 uppercase letter and 1 lowercase letter.'}, 400

    if password.isalpha():
        return {'success': False, 'reason': 'Password should be alphanumeric.'}, 400

    if not any(i.isdigit() for i in password) or not any(i.isalpha() for i in password):
        return {'success': False, 'reason': 'Password should be alphanumeric.'}, 400

    if password.isupper():
        return {'success': False, 'reason': 'Password should contain at least 1 lowercase letter.'}, 400

    if password.islower():
        return {'success': False, 'reason': 'Password should contain at least 1 uppercase letter.'}, 400

    password_hash = generate_password_hash(password)
    user = User(username=username, password=password_hash)
    db.session.add(user)
    db.session.commit()
    return {'success': True, 'reason': 'User is created.'}, 201


@auth.post('/login')
@swag_from('./docs/login.yaml')
def login():
    username = request.json['username']
    password = request.json['password']

    user = User.query.filter_by(username=username).first()

    if user:
        if user.attempt == 5 and user.attempted_at + timedelta(minutes=1) > datetime.now():
            return {'success': False, 'reason': 'Your account is temporarily locked, please retry one minute later.'}, 403

        else:
            if user.attempt == 5 and user.attempted_at + timedelta(minutes=1) < datetime.now():
                user.attempt = 0
                user.attempted_at = None
                db.session.commit()

            is_password_correct = check_password_hash(user.password, password)
            if is_password_correct:
                refresh = create_refresh_token(identity=user.id)
                access = create_access_token(identity=user.id)
                return {'success': True, 'reason': 'Login success.', 'access': access, 'refresh': refresh}, 200

            else:
                user.attempt += 1
                user.attempted_at = datetime.now()
                db.session.commit()
                return {'success': False, 'reason': 'Password is wrong.'}, 401

    return {'success': False, 'reason': 'Username is wrong.'}, 401
