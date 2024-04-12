from app import marsh
from models.movement import MovementModel

class MovementSchema(marsh.SQLAlchemyAutoSchema):

  class Meta:

    model = MovementModel
    load_instance = True