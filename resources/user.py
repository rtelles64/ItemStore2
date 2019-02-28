# adds ability to retrieve User objects from the database
import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()  # get data
    parser.add_argument('username',  # only get username
        type=str,
        required=True,
        help="This field cannot be blank."
    )

    parser.add_argument('password',  # and password
        type=str,
        required=True,
        help="This field cannot be blank."
    )

    def post(self):
        # use data retrieved from parser
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        # user = UserModel(data['username'], data['password'])
        # Since we're always parsing username and password, Python knows to
        #   unpack those values
        user = UserModel(**data)  # this code same as above, using unpacking
        user.save_to_db()

        return {"message": "User created succesffuly."}, 201  # CREATED
