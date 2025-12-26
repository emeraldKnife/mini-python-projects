import sqlite3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

app = Flask(__name__)

# create database
class Base(DeclarativeBase):
  pass

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-database.db"

# create the extension
db = SQLAlchemy(model_class=Base)

# initialise the app with the extention
db.init_app(app)

# create the table
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(500), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    ranking: Mapped[int] = mapped_column(Integer, nullable=False)
    review: Mapped[str] = mapped_column(String(300))
    img_url:Mapped[str] = mapped_column(String(500), nullable=True)

    # optional thingy: this will allow each movies object to be addressed by its title when printed
    def __repr__(self):
      return f'<Movie {self.title}>'
    
# create table schema in the database, requires application context
with app.app_context():
   db.create_all()

# input the data
with app.app_context():
   new_movie = Movie(
      title="`iknowiamfine",
      year=2023,
      description="veryboring",
      rating=3.34,
      ranking=13,
      review="don'tread",
      img_url="https://image.tmdborg/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
   )
   db.session.add(new_movie)
   db.session.commit()
    








# db = sqlite3.connect("books-collection.db")

# cursor = db.cursor()
# cursor.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) NOT NULL, rating FLOAT NOT NULL)")