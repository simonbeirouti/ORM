from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://main_user:123qwe@localhost:5432/orm_tutorial_db"

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Card(db.Model):
    __tablename__ = "cards" 
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    description = db.Column(db.Text())
    date = db.Column(db.Date())
    status = db.Column(db.String())
    priority = db.Column(db.String())
    
class CardSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', 'date', 'status', 'priority')

@app.cli.command('create')
def create_db():
    db.create_all()
    print('Tables created')

@app.cli.command('seed')
def seed_db():
    from datetime import date
    card = Card(
        title = "Start project",
        description = "Step 1 - Create a db",
        date = date.today(),
        status = "To Do",
        priority = "High"
    )
    db.session.add(card)
    db.session.commit()
    print('Table seeded')

@app.route('/')
def index():
    return 'Hello world'

@app.route('/cards')
def cards():
    cards = Card.query.all()
    return CardSchema(many=True).dump(cards)

if __name__ == "__main__": 
    app.run(debug=True)