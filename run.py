from app import app
from db import db

db.init_app(app)

# SQLAlchemy can create our data.db file for us
@app.before_first_request
def create_tables():
    db.create_all()
