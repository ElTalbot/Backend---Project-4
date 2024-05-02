
from models.base import BaseModel, db
from models.user import UserModel
from models.session import SessionModel

class UserSessionModel(db.Model, BaseModel):

    __tablename__ = "user_sessions"


 #  Create the columns 
#  Foreign keys for the user and session
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    session_id = db.Column(db.Integer, db.ForeignKey("sessions.id"))

 # Add the relationships to the UserModel and SessionModel
#  back_populates is identifying which model to create a relationship (ie user with sessions and session with users)
    user = db.relationship("UserModel", back_populates="sessions")
    session = db.relationship("SessionModel", back_populates="users")

