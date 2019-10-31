from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_heroku import Heroku

app = Flask(__name__)
heroku = Heroku(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://woetjbupgiivhu:d1ac4290cdce4bd87c492361aa34eeb69ae87a6bdc2031f55e1b2523a59e1484@ec2-23-21-94-99.compute-1.amazonaws.com:5432/dfnts0vumd52ir"

CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    resort = db.Column(db.String(100))
    rating = db.Column(db.String(100))
    name = db.Column(db.String(100))
    comment = db.Column(db.Text)

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

# @app.route("/reviews/<resort>", methods=["GET"])
# def get_resort(resort):
#     all_reviews = Review.query.get(resort)
#     result = reviews_schema.dump(all_reviews)
#     return jsonify(result)

@app.route("/review", methods=["POST"])
def add_review():
    resort = request.json["resort"]
    rating = request.json["rating"]
    name = request.json["name"]
    comment = request.json["comment"]

    new_review = Review(resort, rating, name, comment)
    db.session.add(new_review)
    db.session.commit()

    created_review = Review.query.get(new_review.id)
    return review_schema.jsonify(created_review)

@app.route("/review/<id>", methods=["PUT"])
def update_review(id):
    review = Review.query.get(id)

    review.resort = request.json["resort"]
    review.rating = request.json["rating"]
    review.name = request.json["name"]
    review.comment = request.json["comment"]

    db.session.commit()
    return review_schema.jsonify(review)

@app.route("/review/<id>", methods=["DELETE"])
def delete_review(id):
    review = Review.query.get(id)

    db.session.delete(review)
    db.session.commit()

    return "RECORD DELETED"

if __name__ == "__main__":
    app.debug = True
    app.run()