from http import HTTPStatus

from flask import Blueprint, request, g 
from marshmallow.exceptions import ValidationError
from middleware.secure_route import secure_route
from models.consent import ConsentformModel
from serializers.consent import ConsentformSchema
# from serializers.user import UserSchema
from app import db


# user_schema = UserSchema()
consent_schema = ConsentformSchema()

router = Blueprint("consent", __name__)

# -----------GET ALL CONSENTFORMS--------------
@router.route("/consentforms", methods=["GET"])
def get_consentforms():

    consentforms = ConsentformModel.query.all()

    return consent_schema.jsonify(consentforms, many=True)


# -----------GET A SINGLE CONSENTFORM-----------
@router.route("/consentforms/<int:consent_id>", methods=["GET"])
def get_single_consent(consent_id):
    consent = ConsentformModel.query.get(consent_id)

    if not consent:
        return {"message": "No Consent Form found"}, HTTPStatus.NOT_FOUND
  
    return consent_schema.jsonify(consent)



# ----------POST A CONSENTFORM--------------
@router.route("/consentforms", methods=["POST"])
@secure_route
def create():
    consent_dictionary = request.json
    
    try:
        consent = consent_schema.load(consent_dictionary)
        consent.user_id = g.current_user.id
        print(consent_dictionary)
        
        consent.save()
        
    except ValidationError as e:
        return {"errors":e.messages, "message": "Something went wrong!"}, HTTPStatus.UNPROCESSABLE_ENTITY
    except Exception as e:
        print(e)
        return {"message": "Something went wrong"}, HTTPStatus.INTERNAL_SERVER_ERROR
    
    
    return consent_schema.jsonify(consent)



# --------DELETE A CONSENTFORM--------------
@router.route("/consentforms/<int:consent_id>", methods=["DELETE"])
@secure_route
def remove(consent_id):
    consent_to_delete = db.session.query(ConsentformModel).get(consent_id)

    if not consent_to_delete:
        return {'message':'Consent Form not found'}, HTTPStatus.NOT_FOUND
    
    if consent_to_delete.user_id != g.current_user.id:
        return {"message": "Unauthorized"}, HTTPStatus.UNAUTHORIZED
  
    consent_to_delete.remove()
    return "", HTTPStatus.NO_CONTENT