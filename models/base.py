from datetime import datetime
from app import db

class BaseModel:

    id = db.Column(db.Integer, primary_key=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def save(self):
        db.session.add(self)
        db.session.commit()

    # ! Added little method to call SQLAlchemy commands to delete my model.
    def remove(self):
        db.session.delete(self)
        db.session.commit()
