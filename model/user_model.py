from db import db
from utils.utils import generate_uuid
import json

class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(20))
    preferred_name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __init__(self, preferred_name, password):
        self.preferred_name = preferred_name
        self.password = password
        self.user_id = generate_uuid()

    def __str__(self):
        return f"<User: ID:{self.id}, Preferred Name:{self.preferred_name}>"

    def to_json(self):
        return {
            "user_id": self.user_id,
            "preferred_name": self.preferred_name,
        }

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "preferred_name": self.preferred_name,
        }

    @classmethod
    def find_by_preferred_name(cls, preferred_name: str) -> 'UserModel':
        return cls.query.filter_by(preferred_name=preferred_name).first()

    @classmethod
    def find_by_uuid(cls, user_id: str) -> 'UserModel':
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def exists_by_user_id(cls, user_id: str) -> 'UserModel':
        return cls.query.filter_by(user_id=user_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()