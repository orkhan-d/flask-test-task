from sqlalchemy import Integer, String, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, validates
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    _tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column()
    balance: Mapped[int] = mapped_column()

    def __init__(self, username: str, balance: int) -> None:
        self.username = username
        self.balance = balance

    @validates('balance')
    def check_balance(self, key: str, value: int):
        if value<5000 or value>15000:
            raise AssertionError({
                'balance': 'balance should be between 5000 and 15000'
            })
        
        return value