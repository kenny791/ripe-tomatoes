from flask import Flask, jsonify
app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

## DB CONNECTION AREA
app.config['SQLALCHEMY_DATABASE_URI']='postgresql+psycopg2://tomato_dev:password123@127.0.0.1:5432/ripe_tomatoes_db'

db = SQLAlchemy(app)
ma = Marshmallow(app)


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

  db.session.commit()
  print('actor seeded')






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

