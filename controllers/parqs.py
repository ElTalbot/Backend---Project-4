from http import HTTPStatus

from flask import Blueprint, request, g 
from marshmallow.exceptions import ValidationError
from middleware.secure_route import secure_route
from models.parq import ParqModel
from serializers.parq import ParqSchema
# from serializers.user import UserSchema
from app import db


# user_schema = UserSchema()
parq_schema = ParqSchema()

router = Blueprint("parqs", __name__)

# -----------GET ALL PARQS--------------
@router.route("/parqs", methods=["GET"])
def get_parqs():

    parqs = ParqModel.query.all()

    return parq_schema.jsonify(parqs, many=True)


# -----------GET A SINGLE PARQ-----------
@router.route("/parqs/<int:parq_id>", methods=["GET"])
def get_single_parq(parq_id):
    parq = ParqModel.query.get(parq_id)

    if not parq:
        return {"message": "No PARQ found"}, HTTPStatus.NOT_FOUND
  
    return parq_schema.jsonify(parq)



# ----------POST A PARQ--------------
@router.route("/parqs", methods=["POST"])
@secure_route
def create():
    parq_dictionary = request.json
    
    try:
        parq = parq_schema.load(parq_dictionary)
        parq.user_id = g.current_user.id
        print(parq_dictionary)
        
        parq.save()
    except ValidationError as e:
        return {"errors":e.messages, "message": "Something went wrong!"}, HTTPStatus.UNPROCESSABLE_ENTITY
    except Exception as e:
        print(e)
        return {"message": "Something went wrong"}, HTTPStatus.INTERNAL_SERVER_ERROR
    
    return parq_schema.jsonify(parq)



# --------DELETE A PARQ--------------
@router.route("/parqs/<int:parq_id>", methods=["DELETE"])
@secure_route
def remove(parq_id):
    parq_to_delete = db.session.query(ParqModel).get(parq_id)

    if not parq_to_delete:
        return {'message':'PARQ not found'}, HTTPStatus.NOT_FOUND
    
    if parq_to_delete.user_id != g.current_user.id:
        return {"message": "Unauthorized"}, HTTPStatus.UNAUTHORIZED
  
    parq_to_delete.remove()
    return "", HTTPStatus.NO_CONTENT