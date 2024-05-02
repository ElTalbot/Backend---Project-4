

import re
from marshmallow import fields, ValidationError
from models.user import UserModel
from app import marsh

def validate_password(password):
    if len(password) <8:
        raise ValidationError("Please make sure your password is at least 8 characters long..")
    elif re.search("[A-Z]", password) is None:
        raise ValidationError("Please make sure your password contains a capital letter..")
  
class UserSchema(marsh.SQLAlchemyAutoSchema):

    movements = fields.Nested("MovementSchema", many=True)
    posts = fields.Nested("PostSchema", many=True)
    sessions = fields.Nested("SessionSchema", many=True)
    parqs = fields.Nested("ParqSchema", many=True)
  
    password = fields.String(required=True, validate=validate_password)

    class Meta:
        model = UserModel
        load_instance = True
        include_fk = True

        exclude = ("password_hash",)

        load_only = ("email", "password")