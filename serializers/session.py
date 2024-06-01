from app import marsh
from models.session import SessionModel
from marshmallow import fields

class SessionSchema(marsh.SQLAlchemyAutoSchema):
    user_id = fields.Int()
    class Meta:
        model = SessionModel
        load_instance = True