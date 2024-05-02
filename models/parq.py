
from models.base import BaseModel, db


class ParqModel(db.Model, BaseModel):

    __tablename__ = "parqs"

    question_one = db.Column(db.Boolean, nullable=False)
    question_two = db.Column(db.Boolean, nullable=False)
    question_three = db.Column(db.Boolean, nullable=False)
    question_four = db.Column(db.Text, nullable=False)
    question_five = db.Column(db.Text, nullable=False)
    question_six = db.Column(db.Text, nullable=False)
    question_seven = db.Column(db.Boolean, nullable=False)
    signed = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship('UserModel', backref="parqs")


  
