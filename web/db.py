from typing import Unpack, TypedDict
from sqlalchemy import Integer, String, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, validates
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UpdateUserArgs(TypedDict, total=False):
    username: str | None
    balance: int | None

class User(db.Model):
    _tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column()
    balance: Mapped[int] = mapped_column()

    def __init__(self, username: str, balance: int) -> None:
        self.username = username
        self.balance = balance

    @staticmethod
    def add_user(username: str, balance: int):
        db.session.add(User(username, balance))
        db.session.commit()

    @staticmethod
    def delete_user(user_id: int):
        db.session.delete(db.session.query(User)\
                          .filter(User.id==user_id).one())
        db.session.commit()

    @staticmethod
    def update_user(user_id: int, **kwargs: Unpack[UpdateUserArgs]):
        user = db.session.query(User)\
                          .filter(User.id==user_id).one()
        
        for k, v in kwargs.items():
            if v:
                user.__setattr__(k, v)
        db.session.commit()

        return user

    @validates('balance')
    def check_balance(self, key: str, value: int):
        if value<5000 or value>15000:
            raise AssertionError({
                'balance': 'balance should be between 5000 and 15000'
            })
        
        return value