from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

db = SQLAlchemy()

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Movie(db.model):
    __moviename__ = "Movies"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, unique=False)
    rating = db.Column(db.Integer, unique=False)
    genre = db.Column(db.String(25), unique=False)
    starring = db.Column(db.String(50), unique=False)

    def __init__(self, title, year, rating, genre, starring):
        self.title = title
        self.year = year
        self.rating = rating
        self.genre = genre
        self.starring = starring

class MovieSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'year', 'rating', 'genre', 'starring')

movie_schema = MovieSchema()
movies_schema = MoviesSchema(many=True)

@app.route("/", methods["GET"])
def home():
    return "<h1>This is a movie db API>"

@app.route("/movies", ["GET"])
def get_movies():
    all_movies = Movie.query.all()
    result = movies_schema.dump(all_movies)
    return jsonify(result)

@app.route("/movie/<id>", methods=["GET"])
def get_movie(id):
    movie = movie.query.get(id)

    result = movie_schema.dump(movie)
    return jsonify(result)

@app.route("/movie", methods=["POST"])
def add_todo():
  title = request.json["title"]
  year = request.json["year"]
  rating = request.json["rating"]
  genre = request.json["genre"]
  starring = request.json["starring"]

  new_movie = Movie(title, title, year, rating, genre, starring)

  db.session.add(new_movie)
  db.session.commit()

  movie = movie.query.get(new_movie.id)
  return todo_schema.jsonify(movie)



# PUT / PATCH
@app.route("/moive/<id>", methods=['PATCH'])  #needs more work
def update_moive(id):
    todo = Todo.query.get(id)

    new_done = request.json["done"]

    todo.done = new_done

    db.session.commit()
    return todo_schema.jsonify(todo)


# DELETE
@app.route("/todo/<id>", methods=["DELETE"])
def delete_todo(id):
    record = Todo.query.get(id)
    db.session.delete(record)
    db.session.commit()

    return jsonify("Its been successfully deleted")

if __name__ == "__main__":
    app.debug = True
    app.run()