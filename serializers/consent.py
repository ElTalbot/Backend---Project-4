from marshmallow import fields
from app import marsh

from models.consent import ConsentformModel

class ConsentformSchema(marsh.SQLAlchemyAutoSchema):
    user_id = fields.Int()
    class Meta:
        
        model = ConsentformModel
        load_instance = True
