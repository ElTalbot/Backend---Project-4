from http import HTTPStatus

from flask import Blueprint, request, g 
from marshmallow.exceptions import ValidationError

from models.session import SessionModel
from models.user import UserModel
from serializers.session import SessionSchema
from serializers.user_session import UserSessionSchema
from serializers.user import UserSchema


session_schema = SessionSchema()
user_session_schema = UserSessionSchema()

router = Blueprint("sessions", __name__)

@router.route("/sessions", methods=["GET"])
def get_sessions():

  sessions = SessionModel.query.all()

  return session_schema.jsonify(sessions, many=True)

