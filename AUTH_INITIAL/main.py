from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here-lol'

# CREATE DATABASE
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# configure flask-login's login manager
login_manager = LoginManager()
login_manager.init_app(app)

# create a user_loader callback
@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

# CREATE TABLE IN DB
# adding the UserMixin
class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method=="POST":
        email = request.form.get('email')
        result = db.session.execute(db.select(User).where(User.email==email))
        user = result.scalar()

        if user:
            flash("you have already signed in with this email, nigga")
            return redirect(url_for('login'))
        
        # hashing and salting the password
        hash_and_salted_pass = generate_password_hash(
            request.form.get('password'),
            method = 'pbkdf2:sha256',
            salt_length=8
        )

        new_user = User(
            email = email,
            password = hash_and_salted_pass,
            name = request.form('name')
        )

        db.session.add(new_user)
        db.session.commit()

        # log in and authenticate the user after adding to the database
        login_user(new_user)

        return redirect(url_for('secrets'))
    
    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=="POST":
        email = request.form.get('email')
        password = request.form.get('password')

        # find user by email
        result = db.session.execute(db.select(User).where(User.email==email))
        user = result.scalar()

        if not user:
            flash("this email, not there, brochacho")
            redirect(url_for('login'))
        elif check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('secrets'))
        else:
            flash("dawg, look at the password again, lol")
            return redirect(url_for('login'))

    return render_template("login.html")

# only loggen in user can access this route
@app.route('/secrets')
@login_required
def secrets():
    print(current_user.name)
    return render_template("secrets.html", name=current_user.name)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/download')
@login_required
def download():
    return send_from_directory('static', path='./files/cheat_sheet.pdf')

if __name__ == "__main__":
    app.run(debug=True)
