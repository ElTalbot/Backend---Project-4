from marshmallow import fields
from models.post import PostModel

from app import marsh

class PostSchema(marsh.SQLAlchemyAutoSchema):

    class Meta:

        model = PostModel
        load_instance = True