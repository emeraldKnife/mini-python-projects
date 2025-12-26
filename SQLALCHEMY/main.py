from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, IntegerField
from wtforms.validators import DataRequired, NumberRange
import requests
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# define the base class for declarative models
class Base(DeclarativeBase):
  pass

# configure the database URI
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies-collection.db" # Renamed DB for clarity

# create the SQLAlchemy db instance
db = SQLAlchemy(model_class=Base)

# initialize the app with the db instance
db.init_app(app)

class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, unique=True, primary_key=True)
    title: Mapped[str] = mapped_column(String(500), unique=True, nullable=True)
    year: Mapped[int] = mapped_column(Integer, nullable=True)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String(300), nullable=True)
    img_url: Mapped[str] = mapped_column(String(500), nullable=True)

    def __repr__(self):
        return f'<Movie {self.title}>'

class edit_movie_form(FlaskForm):
    rating = FloatField("enter the new rating shi, fam", validators=[DataRequired(), NumberRange(min=0, max=10)])
    submit = SubmitField("update the shi")

class add_movie_form(FlaskForm):
    id = IntegerField("gimme the id mann")
    title = StringField("gimme the name typeshi")
    submit = SubmitField("you don't know me son")

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    # this is how you would query the DB (now that it's in scope)
    result = db.session.execute(db.select(Movie))
    all_movies = result.scalars().all()
    return render_template("index.html", movie_collection=all_movies)

@app.route("/edit", methods=['GET', 'POST'])
def edit_card():
    form = edit_movie_form()
    movie_id = request.args.get("id")
    movie = db.get_or_404(Movie, movie_id)
    if form.validate_on_submit():
        movie.rating = float(form.rating.data)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit.html", movie=movie, form=form)

@app.route("/delete", methods=['GET', 'POST'])
def delete_card():
    movie_id = request.args.get("id")
    movie = db.get_or_404(Movie, movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/add", methods=['GET', 'POST'])
def add_card():
    form = add_movie_form()
    if form.validate_on_submit():
        movie_title = form.title.data
        MY_API = "https://api.themoviedb.org/3/search/movie?include_adult=false&language=en-US&page=1"
        MY_API_KEY = os.environ.get("MY_API_KEY")
        parameters = {
            "query": movie_title
        }
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {MY_API_KEY}"
        }
        responce = requests.get(MY_API, params=parameters, headers=headers)
        data = responce.json()
        return render_template("select.html", options=data['results'])
    return render_template("add.html", form=form)

@app.route("/find")
def find_movie():
    movie_id = request.args.get("id")
    if movie_id:
        movie_info_url = "https://api.themoviedb.org/3/movie/"
        movie_api_url = f"{movie_info_url}/{movie_id}"
        MY_API_KEY = os.environ.get("MY_API_KEY")
        parameters = {
            "language": "en-US"
        }
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {MY_API_KEY}"
        }
        response = requests.get(movie_api_url, params=parameters, headers=headers)
        data = response.json()
        movie_img_url = "https://image.tmdb.org/t/p/w500"
        new_movie = Movie(
            title=data["title"],
            year=data["release_date"].split("-")[0],
            img_url=f"{movie_img_url}{data['poster_path']}",
            description=data["overview"]
        )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=True)