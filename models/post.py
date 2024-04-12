from app import db

from models.base import BaseModel
from models.user import UserModel

class PostModel(db.Model, BaseModel):

  __tablename__ = "posts"

  content = db.Column(db.Text, nullable=False, unique=True)

  user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

  user = db.relationship('UserModel', backref="posts")