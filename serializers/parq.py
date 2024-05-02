from marshmallow import fields
from app import marsh

from models.parq import ParqModel

class ParqSchema(marsh.SQLAlchemyAutoSchema):
  
    class Meta:
        
        model = ParqModel
        load_instance = True
