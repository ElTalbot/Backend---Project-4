from app import db
from models.base import BaseModel


class UserSessionModel(db.Model, BaseModel):

  __tablename__ = "user_sessions"


 #  Create the columns
  user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
  session_id = db.Column(db.Integer, db.ForeignKey("sessions.id"))

 # Create the relationships 
  user = db.relationship("UserModel", back_populates="sessions")
  session = db.relationship("SessionModel", back_populates="users")

