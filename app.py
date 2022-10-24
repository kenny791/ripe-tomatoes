from flask import Flask, jsonify, request, abort
app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
from datetime import timedelta

app = Flask(__name__)

## DB CONNECTION AREA
app.config['SQLALCHEMY_DATABASE_URI']='postgresql+psycopg2://tomato_dev:password123@127.0.0.1:5432/ripe_tomatoes_db'
# register JWT secret key
app.config["JWT_SECRET_KEY"] = "Backend best end" 

db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# MODELS AREA

class Movie(db.Model):
  __tablename__ ='movies'
  id = db.Column(db.Integer, primary_key=True)
  title =db.Column(db.String(100))
  genre =db.Column(db.String(50))
  length =db.Column(db.Integer)
  year = db.Column(db.Integer)


class Actor(db.Model):
  __tablename__ ='actors'
  id = db.Column(db.Integer, primary_key=True)
  first_name =db.Column(db.String(100))
  last_name =db.Column(db.String(100))
  gender =db.Column(db.String(20))
  country =db.Column(db.String(50))
  dob =db.Column(db.String(20))


class User(db.Model):
  __tablename__ = "USERS"
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(), nullable=False, unique=True)
  password = db.Column(db.String(), nullable=False)
  is_admin = db.Column(db.Boolean(), default=False)


# SCHEMAS AREA
class MovieSchema(ma.Schema):
  class Meta:
    fields = ('id', 'title','genre','length','year')

class ActorSchema(ma.Schema):
  class Meta:
    fields = ('id', 'first_name','last_name','gender','country','dob')

movie_schema=MovieSchema()
movies_schema=MovieSchema(many=True)
actor_schema=ActorSchema()
actors_schema=ActorSchema(many=True)


class UserSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    fields = ('email','password',"is_admin")

user_schema = UserSchema()
users_schema = UserSchema(many=True)





# CLI COMMANDS AREA
@app.cli.command('drop')
def drop():
  db.drop_all()
  print('table dropped')

@app.cli.command('create')
def create_db():
  db.create_all()
  print('table created')



@app.cli.command('seed')
def seed_db():
  movie1 = Movie(
    title ='Movie title 1',
    genre = 'comedy',
    length = 90,
    year = 2001,
  )
  db.session.add(movie1)
  movie2 = Movie(
    title ='Movie title 2',
    genre = 'action',
    length = 120,
    year = 2002,
  )
  db.session.add(movie2)

  
  # db.session.commit()
  print('movie seeded')

  actor1 = Actor(
    first_name ='FNactor1',
    last_name ='LNactor1',
    gender = 'non-binary',
    country = 'AUS',
    dob = '01.01.01',
)
  db.session.add(actor1)
  
  actor2 = Actor(
    first_name ='FNactor2',
    last_name ='LNactor2',
    gender = 'non-binary',
    country = 'AUS',
    dob = '02.02.02',
)
  db.session.add(actor2)
  
  actor3 = Actor(
    first_name ='FNactor3',
    last_name ='LNactor3',
    gender = 'non-binary',
    country = 'AUS',
    dob = '03.03.03',
)
  db.session.add(actor3)

  actor4 = Actor(
    first_name ='FNactor4',
    last_name ='LNactor4',
    gender = 'non-binary',
    country = 'AUS',
    dob = '04.04.04',
)
  db.session.add(actor4)

  print('actor seeded')

# seed users

  admin=User(
    email='admin@spam.com',
    password=bcrypt.generate_password_hash('eggs').decode('utf-8'),
    is_admin=True
    )
  db.session.add(admin)
  user1=User(
    email='aaa@spam.com',
    password=bcrypt.generate_password_hash('eggs').decode('utf-8'),
    is_admin=False
    )
  db.session.add(user1)


  print('user seeded')

  db.session.commit()


# ROUTING AREA

@app.route("/")
def hello():
  return "Welcome to Ripe Tomatoes API"

@app.route("/movies", methods=['GET'])
def get_movies():
  movies_list = Movie.query.all()
  result = movies_schema.dump(movies_list)
  return jsonify(result)

@app.route("/actors", methods=['GET'])
def get_actors():
  actors_list = Actor.query.all()
  result = actors_schema.dump(actors_list)
  return jsonify(result)

@app.route("/auth/signup", methods=["POST"])
def auth_register():
    #The request data will be loaded in a user_schema converted to JSON. request needs to be imported from
    user_fields = user_schema.load(request.json)
    # find the user
    user = User.query.filter_by(email=user_fields["email"]).first()

    if user:
        # return an abort message to inform the user. That will end the request
        return abort(400, description="Email already registered")
    # Create the user object
    user = User()
    #The request data will be loaded in a user_schema converted to JSON. request needs to be imported from
    user_fields = user_schema.load(request.json)
    #Create the user object
    user = User()
    #Add the email attribute
    user.email = user_fields["email"]
    #Add the password attribute hashed by bcrypt
    user.password = bcrypt.generate_password_hash(user_fields["password"]).decode("utf-8")
    #Add it to the database and commit the changes
    db.session.add(user)
    db.session.commit()
    #Return the user to check the request was successful
    return jsonify(user_schema.dump(user))

#routes declaration area
@app.route("/auth/signin", methods=["POST"])
def auth_login():
    #get the user data from the request
    user_fields = user_schema.load(request.json)
    #find the user in the database by email
    user = User.query.filter_by(email=user_fields["email"]).first()
    # there is not a user with that email or if the password is no correct send an error
    if not user or not bcrypt.check_password_hash(user.password, user_fields["password"]):
        return abort(401, description="Incorrect username and password")

    #create a variable that sets an expiry date
    expiry = timedelta(days=1)
    #create the access token
    access_token = create_access_token(identity=str(user.id), expires_delta=expiry)
    # return the user email and the access token
    return jsonify({"user":user.email, "token": access_token })