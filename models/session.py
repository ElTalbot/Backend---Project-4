from app import db
from models.base import BaseModel
from datetime import datetime, timezone
from models.user_session import UserSessionModel

class SessionModel(db.Model, BaseModel):

  __tablename__ = "sessions"

  name = db.Column(db.Text, nullable=False, unique=True)
  date = db.Column(db.Date, nullable=False, unique=True)
  day = db.Column(db.Text, nullable=False, unique=True)

  user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

  users = db.relationship('UserSessionModel', back_populates="session")



