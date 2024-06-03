from http import HTTPStatus

from datetime import datetime, timezone, timedelta

from flask import Blueprint, request, jsonify, g

import jwt

from marshmallow.exceptions import ValidationError

from models.user import UserModel

from app import db

from serializers.user import UserSchema

from middleware.secure_route import secure_route

from config.environment import SECRET

user_schema = UserSchema()

router = Blueprint('users', __name__)


@router.route('/signup', methods=['POST'])
def signup():
    try:
        user_dictionary = request.json
        print(user_dictionary)
        if user_dictionary["password"] == user_dictionary["confirmPassword"]:
            del user_dictionary["confirmPassword"]
            user_model = user_schema.load(user_dictionary)
            user_model.save()
        

            return user_schema.jsonify(user_model)
        else:
            return{"message": "Passwords do not match"}, HTTPStatus.UNPROCESSABLE_ENTITY
    
    except ValidationError as e:
        return { "errors": e.messages, "message": "Something went wrong!!" }, HTTPStatus.UNPROCESSABLE_ENTITY
    except Exception as e:
        print(e)
        return { "message": "Something went wrong!" }, HTTPStatus.INTERNAL_SERVER_ERROR

@router.route('/login', methods=["POST"])
def login():
    
    credentials_dictionary = request.json

    user = db.session.query(UserModel).filter_by(email=credentials_dictionary["email"]).first()

    if not user:
        return {"message": "Login failed. Please try again"}
    
    if not user.validate_password(credentials_dictionary["password"]):
        return {"message": "Login failed. Please try again"}
    
    payload = {
        "exp": datetime.now(timezone.utc) + (timedelta(days=1)),
        "iat": datetime.now(timezone.utc),
        "sub": user.id,
    }

    token = jwt.encode(
        payload, SECRET, algorithm="HS256"
    )

    return {"message": "Login successful", "token": token}

@router.route('/user', methods=["GET"])
@secure_route
def get_current_user():
    try:
        current_user = UserModel.query.get(g.current_user.id)
        if current_user:
            return user_schema.jsonify(current_user)
    
        else: return jsonify(message="User not found"), HTTPStatus.NOT_FOUND
    except Exception as e:
        print("ERROR", e)
        return jsonify(message="Oh dear, an error occured. Please try again later")
