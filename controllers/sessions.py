from http import HTTPStatus
from sqlalchemy import func
from flask import Blueprint, request, g, jsonify 
from marshmallow.exceptions import ValidationError
from typing import List

from middleware.secure_route import secure_route

from app import db



from models.session import SessionModel
from models.user_session import UserSessionModel
from serializers.session import SessionSchema
from serializers.user_session import UserSessionSchema


session_schema = SessionSchema()
user_session_schema = UserSessionSchema()

router = Blueprint("sessions", __name__)


#  ------------------------ GET ALL SESSIONS --------------------------
# @router.route("/sessions", methods=["GET"])
# def get_sessions():

#     #  Step 1 - need to get all of the sessions
#     sessions = SessionModel.query.all()

#     return session_schema.jsonify(sessions, many=True)
    
#  ------------------------ GET ALL SESSIONS AND USERBOOKING STATUS --------------------------
@router.route("/sessions", methods=["GET"])
@secure_route
def get_sessions_booked_status():

    #  Step 1 - need to get all of the sessions
    sessions = SessionModel.query.all()
    user_id = g.current_user.id

    # Step 2 get the booking status for each session
    sessions_with_status = []
    for session in sessions:
        sessions_with_status.append({
            "session_id": session.id,
            "session_name": session.name,
            "session_date": session.date.strftime('%Y-%m-%d'),
            "session_capacity": session.capacity,
            "user_booked": session.user_booked(),
            "session_day": session.day
        })

    return jsonify({"message": "List of sessions with user booking status", "sessions_with_status": sessions_with_status}), HTTPStatus.OK
    
    # # Step 2 - need to get a list of all the sessions that the user has signed up for
    # current_user_sessions = UserSessionModel.query.filter_by(user_id=user_id).all() 
    # user_session_ids = [user_session.session_id for user_session in current_user_sessions]
    # print("This is the current users session ids i hope:", user_session_ids)

    # # Step 3 - need to combine these so creates object that listss all sessions the current user is signed up for 

    # sessions_info = []
    # for session in sessions:
    #     sessions_info.append({
    #         "session_id": session.id,
    #         "user_booked": session.id in user_session_ids
    #     })

    #     # Step 4 - Combine the list of all sessions with session info
    # combined_sessions: List[ISession] = []
    # for session, info in zip(sessions, sessions_info):
    #     combined_sessions.append({
    #         "session_id": session.id,
    #         "session_name": session.name,  
    #         "user_booked": info["user_booked"],
    #         "session_date": session.date,
    #         "session_capacity": session.capacity
    #     })

    # return jsonify({"message": "List of sessions with user booking status", "combined_sessions": combined_sessions}), 200

    # return jsonify({"message": "List of sessions with user booking status", "sessions_info": sessions_info}), 200
    

# 
#  ------------------------ GET A SINGLE SESSION --------------------------
@router.route("/sessions/<int:session_id>", methods=["GET"])
def get_single_session(session_id):
    session = SessionModel.query.get(session_id)

    if not session:
        return {"message": "No session found"}, HTTPStatus.NOT_FOUND
  
    return session_schema.jsonify(session)

# -------------------------GET ALL USERSESSIONS BY SESSIONID--------------------
@router.route("/usersessions/<int:session_id>", methods=["GET"])
def get_usersessions(session_id):


    user_count = (db.session.query(func.count(UserSessionModel.user_id.distinct())).filter(UserSessionModel.session_id == session_id).scalar())
    print(user_count)

    return jsonify({'user_count': user_count})



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
    session_id = data.get("session_id")

    session_to_book = SessionModel.query.get(session_id)

    if not session_to_book:
        return {"message": "No session found"}, HTTPStatus.NOT_FOUND

    num_booked_users = (
        db.session.query(func.count(UserSessionModel.user_id.distinct()))
        .filter(UserSessionModel.session_id == session_to_book.id)
        .scalar()
    )
    if num_booked_users >= session_to_book.capacity:
        return {"message": "Apologies, this session is already full"}, HTTPStatus.UNAUTHORIZED

    user_session = UserSessionModel(user_id=user_id, session_id=session_id)
    user_session.save()

    return {"message": "User successfully added to the session"}, HTTPStatus.OK
    
    
   

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