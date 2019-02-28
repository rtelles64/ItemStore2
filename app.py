# This template provides a RESTful structure
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

# NOTE: we no longer use jsonify since flask_restful does it for us

app = Flask(__name__)

# tell SQLAlchemy where to find data.db
# NOTE: sqlite does not have to be sqlite:
#   it can be:
#       - MySQL
#       - PostGre SQL
#       - Oracle
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  # lives in root

# turn off Flask SQLAlchemy modification tracker
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# NOTE: if this is a production API, the secret_key should be hidden
app.secret_key = "81h2459gpasiubdglkqwy97ryqhou!@##%@#^"
api = Api(app)  # easily add resources to our API

# SQLAlchemy can create our data.db file for us
@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity)  # /auth

# ADD RESOURCE (with route)
# http://127.0.0.1:5000/item/name
api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':  # prevents from running app.py if it is an import
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)  # port 5000 is the default but it's nice to
    #                                  get practice
