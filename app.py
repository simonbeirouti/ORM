from datetime import timedelta
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow.validate import Length
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://db_dev:123qwe@localhost:5432/trello_clone_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'aa889ce3-8f92-4d01-93a7-f59cb2672392'

db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

class Card(db.Model):
    __tablename__ = 'cards'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    description = db.Column(db.Text())
    date = db.Column(db.Date())
    status = db.Column(db.String())
    priority = db.Column(db.String())
    
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable = False, unique = True)
    password = db.Column(db.String(), nullable = False)
    admin = db.Column(db.Boolean(), default = False)

class CardSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', 'date', 'status', 'priority')

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'email', 'password', 'password', 'admin')
    password = ma.String(validate=Length(min=8))

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.cli.command('create')
def create_db():
    db.create_all()
    print('Tables created')

@app.cli.command('drop')
def drop_db():
    db.drop_all()
    print('Database dropped')

@app.cli.command('seed')
def seed_db():
    from datetime import date
    card = Card(
        title = 'Start project',
        description = 'Step 1 - Create a db',
        date = date.today(),
        status = 'To Do',
        priority = 'High'
    )
    admin = User(
        email = 'hi@email.com',
        password = bcrypt.generate_password_hash('123qwe123').decode('utf-8'),
        admin = True
    )
    user1 = User(
        email = 'bye@email.com',
        password = bcrypt.generate_password_hash('123qwe123').decode('utf-8'),
    )
    db.session.add(card)
    db.session.add(admin)
    db.session.add(user1)
    db.session.commit()
    print('Table seeded')

@app.route('/')
def index():
    return 'Hello world'

@app.route('/cards', methods=['GET'])
@jwt_required()
def cards():
    cards = Card.query.all()
    result = CardSchema(many=True).dump(cards)
    return result

@app.route('/auth/register', methods=['POST'])
def auth_register():
    user_fields = user_schema.load(request.json)
    user = User(
        email = user_fields['email'],
        password = bcrypt.generate_password_hash(user_fields['password']).decode('utf-8')
    )
    db.session.add(user)
    db.session.commit()
    access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
    return jsonify({"user": user.email, "token": access_token})

@app.route('/auth/login', methods=['POST'])
def auth_login():
    user_fields = user_schema.load(request.json)
    user = User.query.filter_by(email = user_fields['email']).first()
    if not user or not bcrypt.check_password_hash(user.password, user_fields['password']):
        return abort(401, description = 'Invalid email or password')
    access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
    return jsonify({"user": user.email, "token": access_token})

if __name__ == '__main__': 
    app.run(debug=True)