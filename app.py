from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_heroku import Heroku

app = Flask(__name__)
heroku = Heroku(app)

app.config["SQLALCHEMY_DATABASE_URI"] = ""

CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    resort = db.Column(db.String(100))
    rating = db.Column(db.String(100))
    name = db.Column(db.String(100))
    comment = db.Column(db.Blob)

    def __init__(self, resort, rating, name, comment):
        self.resort = resort
        self.rating = rating
        self.name = name
        self.comment = comment

class ReviewSchema(ma.Schema):
    class Meta: 
        fields = ("id", "resort", "rating", "name", "comment")

review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)


@app.route("/reviews", methods=["GET"])
def get_reviews():
    all_reviews = Review.query.all()
    result = reviews_schema.dump(all_reviews)
    return jsonify(result)

@app.route("/review", methods=["POST"])
def add_todo():
    title = request.json["title"]
    done = request.json["done"]

    new_todo = Todo(title, done)
    db.session.add(new_todo)
    db.session.commit()

    created_todo = Todo.query.get(new_todo.id)
    return todo_schema.jsonify(created_todo)

@app.route("/todo/<id>", methods=["PUT"])
def update_todo(id):
    todo = Todo.query.get(id)

    todo.title = request.json["title"]
    todo.done = request.json["done"]

    db.session.commit()
    return todo_schema.jsonify(todo)

@app.route("/todo/<id>", methods=["DELETE"])
def delete_todo(id):
    todo = Todo.query.get(id)

    db.session.delete(todo)
    db.session.commit()

    return "RECORD DELETED"

if __name__ == "__main__":
    app.debug = True
    app.run()