from app import db
from models.base import BaseModel
from models.user import UserModel


class MovementModel(db.Model, BaseModel):

  __tablename__ = "movements"

  name = db.Column(db.Text, nullable=False)
  descriptionOne = db.Column(db.Text, nullable=False)
  descriptionTwo = db.Column(db.Text)
  descriptionThree = db.Column(db.Text)
  descriptionFour = db.Column(db.Text)
  descriptionFive = db.Column(db.Text)
  descriptionSix = db.Column(db.Text)
  image = db.Column(db.Text, nullable=False)
  type = db.Column(db.Text, nullable=False)
  equipment = db.Column(db.Text, nullable=False)
  video = db.Column(db.Text, nullable=False)
  adaption = db.Column(db.Text, nullable=False)
  

  user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

  user = db.relationship('UserModel', backref="movements")
  
