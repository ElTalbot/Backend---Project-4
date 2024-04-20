from http import HTTPStatus
from sqlalchemy import func
from flask import Blueprint, request, g 
from marshmallow.exceptions import ValidationError

from middleware.secure_route import secure_route

from app import db



from models.session import SessionModel
from models.user import UserModel
from models.user_session import UserSessionModel
from serializers.session import SessionSchema
from serializers.user_session import UserSessionSchema
from serializers.user import UserSchema


session_schema = SessionSchema()
user_session_schema = UserSessionSchema()

router = Blueprint("sessions", __name__)


#  ------------------------ GET ALL SESSIONS --------------------------
@router.route("/sessions", methods=["GET"])
def get_sessions():

    sessions = SessionModel.query.all()

    return session_schema.jsonify(sessions, many=True)

#  ------------------------ GET A SINGLE SESSION --------------------------
@router.route("/sessions/<int:session_id>", methods=["GET"])
def get_single_session(session_id):
    session = SessionModel.query.get(session_id)

    if not session:
        return {"message": "No session found"}, HTTPStatus.NOT_FOUND
  
    return session_schema.jsonify(session)

#  ------------------------ POST A SESSION --------------------------
@router.route("/sessions", methods=["POST"])
@secure_route
def create():
    session_dictionary = request.json
  

    try:
        session = session_schema.load(session_dictionary)
        session.user_id = g.current_user.id
        session.save()
    
        sessions = db.session.query(SessionModel).all()
        return session_schema.jsonify(sessions, many=True)
    
    except ValidationError as e:
        return {"errors": e.messages, "message": "Something went wrong!"}, HTTPStatus.UNPROCESSABLE_ENTITY
    except Exception as e: 
        print(e)
        return {"message": "Something went wrong"}, HTTPStatus.INTERNAL_SERVER_ERROR
  
#  ------------------------ DELETE A SESSION --------------------------
@router.route("/sessions/<int:session_id>", methods=["DELETE"])
@secure_route
def remove(session_id):
    session_to_delete = db.session.query(SessionModel).get(session_id)

    if not session_to_delete:
        return {'message':'Session not found'}, HTTPStatus.NOT_FOUND
    
    if session_to_delete.user_id != g.current_user.id:
        return {"message": "Unauthorized"}, HTTPStatus.UNAUTHORIZED
  
    session_to_delete.remove()
    return "", HTTPStatus.NO_CONTENT

#  ------------------------ UPDATE A SESSION --------------------------
@router.route("/sessions/<int:session_id>", methods=["PUT", "PATCH"])
@secure_route
def update_session(session_id):
    session_dictionary = request.json

    existing_session = SessionModel.query.get(session_id)

    if not existing_session:
        return {"message": "No session found"}, HTTPStatus.NOT_FOUND
   
    try:
        if existing_session.user_id != g.current_user.id:
            return { "message": "This is not your session! Maybe try another" }, HTTPStatus.UNAUTHORIZED

        session = session_schema.load(
           session_dictionary,
           instance=existing_session, 
           partial=True
        )

        session.save()
    except ValidationError as e:
        return {"errors": e.messages, "message": "Something went wrong"}
    return session_schema.jsonify(session), HTTPStatus.OK

#  ------------------------ BOOK A SESSION --------------------------
@router.route("/sessions/book", methods=["POST"])
@secure_route
def book_session():
  
    data = request.json
    user_id = g.current_user.id
  #  user_id = data.get("user_id")
    session_id = data.get("session_id")

    session_to_book = SessionModel.query.get(session_id)


    if not session_to_book:
        return {"message": "No session found"}, HTTPStatus.NOT_FOUND
   
    num_booked_users = ( db.session.query(func.count(UserSessionModel.user_id.distinct()))
    .filter(UserSessionModel.session_id == session_to_book.id)
    .scalar())
    if num_booked_users >= session_to_book.capacity:
        return {"message": "Apologies, this session is already full"}, HTTPStatus.UNAUTHORIZED
   
    user_session = UserSessionModel(user_id=user_id, session_id=session_id)
    user_session.save()

  #  Step 1 - need to get all of the sessions
    all_sessions = SessionModel.query.all()
    # print(all_sessions)

    # Step 2 - need to get a list of all the sessions that the user has signed up for
    current_user_sessions = UserSessionModel.query.filter_by(user_id=user_id).all() 
    user_session_ids = [user_session.session_id for user_session in current_user_sessions]
    # print("This is the current users session ids i hope:", user_session_ids)

    # Step 3 - need to combine these so creates object that listss all sessions the current user is signed up for 
    # Function needs to return all of the sessions with the user_id
    def users_booked_sessions(session):
        return {"session_id": session.id,
        "user_booked": session.id in user_session_ids}
    
    bookings = map(users_booked_sessions, all_sessions)
    bookings_list = list(bookings)
    print("Bookings list:", bookings_list)



    return {"user_session_ids":user_session_ids, "bookings_list":bookings_list}, HTTPStatus.OK

#  ------------------------ CANCEL A SESSION --------------------------
@router.route("/sessions/cancel", methods=["DELETE"])
@secure_route
def cancel_session():
  
    data = request.json
    user_id = g.current_user.id
  #  user_id = data.get("user_id")
    session_id = data.get("session_id")

    user_session = UserSessionModel.query.filter_by(user_id=user_id, session_id=session_id).first()


    if not user_session:
        return {"message": "No session found"}, HTTPStatus.NOT_FOUND
   
    user_session.remove()

    return {"message": "Sorry to see you have cancelled, hopefully see you next time."}, HTTPStatus.OK