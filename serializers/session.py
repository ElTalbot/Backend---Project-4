from app import marsh
from models.session import SessionModel

class SessionSchema(marsh.SQLAlchemyAutoSchema):

  class Meta:
    model = SessionModel
    load_instance = True