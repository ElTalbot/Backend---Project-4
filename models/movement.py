from app import db
from models.base import BaseModel
from models.user import UserModel


class MovementModel(db.Model, BaseModel):

  __tablename__ = "movements"

  name = db.Column(db.Text, nullable=False, unique=True)
  description = db.Column(db.Text, nullable=False, unique=True)
  image = db.Column(db.Text, nullable=False, unique=True)
  type = db.Column(db.Text, nullable=False, unique=True)
  equipment = db.Column(db.Text, nullable=False, unique=True)
  video = db.Column(db.Text, nullable=False, unique=True)
  adaption = db.Column(db.Text, nullable=False, unique=True)
  

  user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

  user = db.relationship('UserModel', backref="movements")
  
