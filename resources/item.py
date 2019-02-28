from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

# CRUD
# Most API's follow the CRUD method
# - Create - POST
# - Read - GET
# - Update - PUT
# - Delete - DELETE

# EVERY RESOURCE HAS TO BE A CLASS
class Item(Resource):
    parser = reqparse.RequestParser()
    # ensure that we only parse requests by price
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store id."
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            return item.json()

        return {"message": "Item not found"}, 404

    # POPULAR INTERVIEW QUESTION:
    # "What's the  most popular http status code? 404 (NOT 200!)"

    def post(self, name):  # this has to have the same method signature!
        # ERROR FIRST APPROACH
        if ItemModel.find_by_name(name):
            # 400: SOMETHING WENT WRONG WITH THE REQUEST
            return ({"message": f"An item with name '{name}' already exists"},
                    400)

        # data = request.get_json() REPLACED BY .parse_args()
        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            # 500: INTERNAL SERVER ERROR
            return {"message": "An error occurred inserting item."}, 500

        return item.json(), 201  # lets client (application) know this happened
        # 201 code is a CREATED status

    def delete(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            item.delete_from_db()

        return {"message": "Item deleted"}

    def put(self, name):
        data = Item.parser.parse_args()
        # check if item exists
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        # With lambda (used if programming in other languages):
        # {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
        # With list comprehension (more Pythonic):
        return {'items': [item.json() for item in ItemModel.query.all()]}
