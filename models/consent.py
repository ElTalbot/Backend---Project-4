from models.base import BaseModel, db


class ConsentformModel(db.Model, BaseModel):

    __tablename__ = "consentforms"

    question_one = db.Column(db.Boolean, nullable=False)
    question_two = db.Column(db.Boolean, nullable=False)
    question_three = db.Column(db.Boolean, nullable=False)
    question_four = db.Column(db.Boolean, nullable=False)
    question_five = db.Column(db.Boolean, nullable=False)
    question_six = db.Column(db.Boolean, nullable=False)
    question_seven = db.Column(db.Boolean, nullable=False)
    question_eight = db.Column(db.Boolean, nullable=False)
    signed = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship('UserModel', backref="consentforms")
