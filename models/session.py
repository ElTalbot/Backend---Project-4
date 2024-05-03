from datetime import datetime, timezone
from app import db
from flask import g

from models.base import BaseModel



class SessionModel(db.Model, BaseModel):

    __tablename__ = "sessions"

    name = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False, unique=True)
    day = db.Column(db.Text, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    users = db.relationship('UserSessionModel', back_populates="session")

    def user_booked(self):
        from models.user_session import UserSessionModel

        user_id = g.current_user.id
        return bool(UserSessionModel.query.filter_by(session_id=self.id, user_id=user_id).first())
