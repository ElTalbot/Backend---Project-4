
from datetime import datetime, timedelta, timezone

import jwt

from sqlalchemy.ext.hybrid import hybrid_property

from config.environment import SECRET
from models.base import BaseModel, db
from app import bcrypt



class UserModel(db.Model, BaseModel):

    __tablename__ = "users"

    username = db.Column(db.Text, nullable=False, unique=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    is_admin = db.Column(db.Text, nullable=True)

    password_hash = db.Column(db.Text, nullable=True)

    sessions = db.relationship("UserSessionModel", back_populates="user")


    @hybrid_property
    def password(self):
        pass

    @password.setter
    def password(self, password_plaintext):
        encoded_hashed_pw = bcrypt.generate_password_hash(password_plaintext)
        self.password_hash = encoded_hashed_pw.decode("utf-8")

    
    def validate_password(self, login_password):
        return bcrypt.check_password_hash(self.password_hash, login_password)
  
  # def generate_token(self):

  #     payload = {
  #         "exp": datetime.fromtimestamp(timezone.utc) + timedelta(days=2),
  #         "iat": datetime.fromtimestamp(timezone.utc),
  #         "sub": self.id
  #       }

  #     token = jwt.encode(
  #         payload,
  #         SECRET,
  #         algorithm="HS256"
  #       )

  #     return token