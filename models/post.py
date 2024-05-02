from sqlalchemy import DateTime


from models.base import BaseModel, db


class PostModel(db.Model, BaseModel):

    __tablename__ = "posts"

    content = db.Column(db.Text, nullable=False, unique=True)

     # The foreign key tells you which column to point at (users.id),
     # so that every post points to a specific unique user
     # This defines the relationship between the post and the user

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship('UserModel', backref="posts")