# NOTE: This UserModel is an API! (not RESTful mind you)
#   - find_by_username() and find_by_id() are interfaces that allow other parts
#      of our program to interact with the User
import sqlite3
from db import db

class UserModel(db.Model):
    __tablename__ = 'users'

    # table columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        # self.id (or self.var_name) must equal the name of the columns
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod  # since we don't use self anywhere but only the class name
    def find_by_username(cls, username):
        # filter_by(table_column_name=argument)
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
