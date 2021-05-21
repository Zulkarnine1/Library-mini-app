from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from flask_sqlalchemy import SQLAlchemy





app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250),unique=True,nullable=False)
    author = db.Column(db.String(250),nullable=False)
    rating = db.Column(db.Float,nullable=False)

    def __repr__(self):
        return '<Book %r>' % self.title


db.create_all()

@app.route('/')
def home():
    books = Book.query.all()
    return render_template("index.html", all_books=books ,length = len(books))


@app.route("/add",methods=["Get","Post"])
def add():
    if request.method == "GET":
        return render_template("add.html")
    else:
        name = request.form["name"]
        author = request.form["author"]
        rating = request.form["rating"]
        harry = Book(title=name, author=author, rating=rating)
        db.session.add(harry)
        db.session.commit()
        return redirect("/")

@app.route("/edit/<id>",methods=["Get","Post"])
def edit(id):
    if request.method == "GET":
        book = Book.query.filter_by(id=id).first()
        return render_template("edit.html",book=book)
    else:
        book = Book.query.filter_by(id=id).first()
        name = request.form["name"]
        author = request.form["author"]
        rating = request.form["rating"]
        book.name = name
        book.author = author
        book.rating = rating
        db.session.commit()
        return redirect("/")


@app.route("/delete",methods=["Get"])
def delete():
    book_id = request.args.get('id')
    book = Book.query.filter_by(id=book_id).first()
    db.session.delete(book)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)

