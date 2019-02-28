# Demonstrating how we can add to our API
from db import db


class StoreModel(db.Model):  # tell SQLAlchemy entity that this is a model
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    # many to one relationship: items is essentially a list of ItemModels
    # lazy = dynamic - self.items becomes a query builder
    items = db.relationship('ItemModel', lazy='dynamic')  # connect ItemModel

    def __init__(self, name):
        self.name = name

    def json(self):
        '''
        Returns json representation of the ItemModel
        '''
        return {'name': self.name,
                'items': [item.json() for item in self.items.all()]
                }

    @classmethod
    def find_by_name(cls, name):
        '''
        Returns item by name
        :param name: name to be searched for
        '''
        # .query() comes from SQLAlchemy
        # .first() returns first row only
        # SQL Translation:
        #   SELECT * FROM items WHERE name=name LIMIT 1
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        '''
        Saves item to database
        '''
        # SQLAlchemy knows how to add objects to the database
        # .session is a collection of objects that we write to the database
        # we can first add multiple then commit them all at once, but in this
        # case we just add one
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
