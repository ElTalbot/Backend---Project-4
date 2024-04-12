from app import marsh
from models.post import PostModel
from serializers.user import UserSchema
from marshmallow import fields

class PostSchema(marsh.SQLAlchemyAutoSchema):

  class Meta:

    model = PostModel
    load_instance = True