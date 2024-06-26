from app import marsh

from models.user_session import UserSessionModel

from marshmallow import fields

class UserSessionSchema(marsh.SQLAlchemyAutoSchema):

    session = fields.Nested("SessionSchema")
    user_id = fields.Int()

    class Meta:

        include_fk = True
        model = UserSessionModel
        load_instance = True