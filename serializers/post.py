from marshmallow import fields
from models.post import PostModel

from app import marsh

class PostSchema(marsh.SQLAlchemyAutoSchema):
    user_id = fields.Int()
    username = fields.String(attribute="user.username")

    class Meta:

        model = PostModel
        load_instance = True