
from marshmallow import fields
from models.movement import MovementModel
from app import marsh

class MovementSchema(marsh.SQLAlchemyAutoSchema):
    
    user_id = fields.Int()

    class Meta:

        model = MovementModel
        load_instance = True