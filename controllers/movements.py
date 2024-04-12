from http import HTTPStatus
from app import db

from middleware.secure_route import secure_route
from flask import Blueprint, request, g 
from marshmallow.exceptions import ValidationError

from models.movement import MovementModel
from models.user import UserModel
from serializers.movement import MovementSchema
from serializers.user import UserSchema

movement_schema = MovementSchema()
UserSchema = UserSchema()

router = Blueprint("movements", __name__)

#  ------------------------ GET ALL MOVEMENTS --------------------------
@router.route("/movements", methods=["GET"])
def get_movements():

  movements = MovementModel.query.all()

  return movement_schema.jsonify(movements, many=True)

#  ------------------------ GET A SINGLE MOVEMENT --------------------------
@router.route("/movements/<int:movement_id>", methods=["GET"])
def get_single_movement(movement_id):
  movement = MovementModel.query.get(movement_id)

  if not movement:
    return {"message": "No movement found"}, HTTPStatus.NOT_FOUND
  
  return movement_schema.jsonify(movement)

#  ------------------------ POST A MOVEMENT --------------------------
@router.route("/movements", methods=["POST"])
@secure_route
def create():
  movement_dictionary = request.json
 
  

  try:
    movement = movement_schema.load(movement_dictionary)
    movement.user_id = g.current_user.id
    print(movement_dictionary)
    movement.save()
    
    movements = db.session.query(MovementModel).all()
    return movement_schema.jsonify(movements, many=True)
  
  except ValidationError as e:
    return {"errors": e.messages, "message": "Something went wrong!"}, HTTPStatus.UNPROCESSABLE_ENTITY
  except Exception as e: 
    print(e)
    return {"message": "Something went wrong"}, HTTPStatus.INTERNAL_SERVER_ERROR
  
#  ------------------------ DELETE A MOVEMENT --------------------------
@router.route("/movements/<int:movement_id>", methods=["DELETE"])
@secure_route
def remove(movement_id):
  movement_to_delete = db.session.query(MovementModel).get(movement_id)

  if not movement_to_delete:
        return {'message':'Movement not found'}, HTTPStatus.NOT_FOUND
    
  if movement_to_delete.user_id != g.current_user.id:
        return {"message": "Unauthorized"}, HTTPStatus.UNAUTHORIZED
  
  movement_to_delete.remove()
  return "", HTTPStatus.NO_CONTENT

  #  ------------------------ UPDATE A MOVEMENT --------------------------
@router.route("/movements/<int:movement_id>", methods=["PUT", "PATCH"])
@secure_route
def update_movement(movement_id):
   movement_dictionary = request.json

   existing_movement = MovementModel.query.get(movement_id)

   if not existing_movement:
       return {"message": "No movement found"}, HTTPStatus.NOT_FOUND
   
   try:
       if existing_movement.user_id != g.current_user.id:
           return { "message": "This is not your movement! Maybe try another" }, HTTPStatus.UNAUTHORIZED

       movement = movement_schema.load(
           movement_dictionary,
           instance=existing_movement, 
           partial=True
        )

       movement.save()
   except ValidationError as e:
        return {"errors": e.messages, "message": "Something went wrong"}
   return movement_schema.jsonify(movement), HTTPStatus.OK
