from app import db
from models.base import BaseModel
from datetime import datetime, timezone
from models.user_session import UserSessionModel
from models.user import UserModel

class SessionModel(db.Model, BaseModel):

  __tablename__ = "sessions"

  name = db.Column(db.Text, nullable=False)
  date = db.Column(db.Date, nullable=False, unique=True)
  day = db.Column(db.Text, nullable=False)
  capacity = db.Column(db.Integer, nullable=False)

  user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
  # user = db.relationship("UserModel", back_populates="session")

  users_book = db.relationship('UserSessionModel', back_populates="session")



