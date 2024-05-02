from marshmallow import fields
from app import marsh

from models.consent import ConsentformModel

class ConsentformSchema(marsh.SQLAlchemyAutoSchema):
  
    class Meta:
        
        model = ConsentformModel
        load_instance = True
