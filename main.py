from datetime import date
from typing import List
import werkzeug
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from flask import Flask, abort, render_template, redirect, url_for, flash, request, session as flask_session
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from forms import EditForm, DeleteForm, AddForm, LoginForm, RegisterForm
import requests
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Integer, String, Text, ForeignKey, UniqueConstraint
from bs4 import BeautifulSoup
import smtplib
import os
from dotenv import load_dotenv
import logging
from flask_session import Session

load_dotenv()



app = Flask(__name__)
class Config:
    SECRET_KEY = os.getenv("APP_CONFIG_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///movies_base.db")


app.config.from_object(Config)

handler = logging.FileHandler(".venv/app.log", encoding="utf-8")
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

ckeditor = CKEditor(app)
Bootstrap5(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "warning"
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = "./.flask_session/"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True

Session(app)
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))



db = SQLAlchemy(app)
headers = {
            "accept": "application/json",
            "Authorization": os.getenv("TMDB_BEARER")
        }
header = {"Accept-Language":"en-GB",
          "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0"}

URL= "https://screenrant.com/movie-news/"
password = os.getenv('PASSWORD')
class Movies(db.Model):
    __tablename__ = "movies"
    __table_args__ = (
        UniqueConstraint("user_id", "title", name="uq_user_movie_title"),
    )
    id:Mapped[int] = db.Column("id", db.Integer, primary_key=True)
    title:Mapped[str] = db.Column("title", db.VARCHAR(250), nullable=False)
    year:Mapped[int] = db.Column("year", db.Integer)
    description: Mapped[str] = db.Column("description", db.Text)
    rating: Mapped[float] = db.Column("rating", db.Float)
    ranking: Mapped[int] = db.Column("ranking", db.Integer)
    review: Mapped[str] = db.Column("review", db.Text)
    img_url: Mapped[str] = db.Column("img_url", db.VARCHAR(250))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="movies")

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))
    role: Mapped[str] = mapped_column(String(20), default="user")
    movies = relationship("Movies", back_populates="owner", cascade="all, delete-orphan")

with app.app_context():
    db.create_all()
    
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != "admin":
            return abort(403)
        return f(*args, **kwargs)

    return decorated_function

@app.route('/', methods=["GET","POST"])
def home():
    images, titles, article_link = [], [], []
    try:
        response = requests.get(URL, headers=header, timeout=8)
        response.raise_for_status()
        yc_web_page = response.text
        soup = BeautifulSoup(yc_web_page, "html.parser")
        article = soup.find_all(name="a", class_="bc-title-link")
        img = soup.find_all(name="a", class_="bc-img-link")

        if article:
            images = [source.get("srcset") for source in soup.select("picture source")[3::4]]
            titles = [x.get("title") for x in article]
            article_link = [y.get("href") for y in img]
    except requests.RequestException as e:
        app.logger.exception(" Cannot download the News! ", e)
        flash(" Cannot download the News!", "danger")

    return render_template("home.html", images=images, titles=titles, article_link=article_link)




@app.route('/newmovies', methods=["GET","POST"])
def new_movies():
    params = {"page": 1, "sort_by": "popularity.desc", "language": "en-US", "include_adult": False, "include_video": False}
    url = "https://api.themoviedb.org/3/discover/movie"
    try:
        response = requests.get(url, headers=headers, params=params, timeout=8)
        response.raise_for_status()
        xresponse = response.json().get("results", [])
    except requests.RequestException as e:
        app.logger.exception(" Cannot download the Movie list! ", e)
        flash(" Cannot download the Movie list! ", "danger")
        xresponse = []

    img_url = [x.get('backdrop_path') for x in xresponse]
    title = [x.get('title') for x in xresponse]
    year = [x.get('release_date') for x in xresponse]
    descript = [x.get('overview') for x in xresponse]
    return render_template("newmovies.html", title=title, year=year, descript=descript, img_url=img_url)


@app.route('/new_tv', methods=["GET","POST"])
def new_tv():
    params = {"page": 1, "sort_by": "popularity.desc", "language": "en-US", "include_adult": False, "include_video": False}
    url = "https://api.themoviedb.org/3/discover/tv"
    try:
        response = requests.get(url, headers=headers, params=params, timeout=8)
        response.raise_for_status()
        xresponse = response.json().get("results", [])
    except requests.RequestException as e:
        app.logger.exception(" Cannot download list of TV Series! ", e)
        flash(" Cannot download list of  TV Series! ", "danger")
        xresponse = []

    img_url = [x.get('backdrop_path') for x in xresponse]
    title = [x.get('name') for x in xresponse]
    year = [x.get('first_air_date') for x in xresponse]
    descript = [x.get('overview') for x in xresponse]
    return render_template("new-tv.html", title=title, year=year, descript=descript, img_url=img_url)



@app.route('/movie_rank', methods=["GET","POST"])
@login_required
def movie_rank():
    delete_form = DeleteForm()
    all_movies = db.session.execute(
        db.select(Movies).where(Movies.user_id == current_user.id)
    ).scalars().all()


    all_movies.sort(key=lambda m: (m.rating or 0), reverse=True)
    for i, movie in enumerate(all_movies, start=1):
        movie.ranking = i
    db.session.commit()
    return render_template("movie_rank.html", movies=all_movies, delete_form=delete_form)

@app.route('/add', methods=["GET", "POST"])
@login_required
def add():
    form = AddForm()
    if form.validate_on_submit():
        add_movie = form.add.data
        url = f"https://api.themoviedb.org/3/search/movie?query={add_movie}&include_adult=false&language=en-US&page=1"
        response = requests.get(url, headers=headers)
        data = response.json().get("results", [])

        flask_session['new_record'] = [
            {
                "id": m.get("id"),
                "title": m.get("title"),
                "release_date": m.get("release_date"),
                "overview": m.get("overview"),
                "backdrop_path": m.get("backdrop_path"),
            }
            for m in data
        ]
        return redirect(url_for("select"))
    return render_template("add.html", form=form)



@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    form = EditForm()
    movie_id = request.form.get("movie_id") or request.args.get("movie_id")
    print(movie_id)
    name = db.session.execute(db.select(Movies).filter_by(id=movie_id)).scalar_one_or_none()
    print(name)
    if form.validate_on_submit():
        rating_input = form.rating.data
        review_input = form.review.data
        name.rating = float(rating_input)
        name.review = review_input
        db.session.commit()
        return redirect(url_for("movie_rank", movie_name=name.title))
    return render_template("edit.html",form=form, name=name)

@app.route('/delete',methods=["POST"])
@login_required
def delete():
    form = DeleteForm()
    movie_id = request.form.get("movie_id") or request.args.get("movie_id")
    name = db.session.execute(db.select(Movies).filter_by(id=movie_id)).scalar_one_or_none()
    if form.validate_on_submit():
        db.session.delete(name)
        db.session.commit()
    return redirect(url_for("movie_rank"))

@app.route('/select', methods=["GET", "POST"])
@login_required
def select():
    result = flask_session.get('new_record') or []
    if not result:
        flash("No results! ", "warning")
        return redirect(url_for("add"))

    how_many = len(result)
    movie_id = request.form.get("movie_id") or request.args.get("movie_id")

    if movie_id:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
        try:
            response = requests.get(url, headers=headers, timeout=8)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            app.logger.exception(" We cannot download movie details! ", e)
            flash(" We cannot download movie details! ", "danger")
            return redirect(url_for("select"))

        img_path = data.get('backdrop_path')
        img_url = f"https://image.tmdb.org/t/p/w500/{img_path}" if img_path else None
        title = data.get('title')
        year = (data.get('release_date') or "")[:4]
        descript = data.get('overview')

        another_movie = Movies(
            title=title,
            year=year if year.isdigit() else None,
            description=descript,
            rating=0,
            img_url=img_url,
            user_id=current_user.id,
        )
        db.session.add(another_movie)
        db.session.commit()
        return redirect(url_for("movie_rank"))

    return render_template("select.html", result=result, how_many=how_many)




@app.route('/login', methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('home'))

    return render_template("login.html", form=form, current_user=current_user)

@app.route('/signup', methods=["GET","POST"])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()
        if user:
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('signup'))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("home"))
    return render_template("signup.html", form=form, current_user=current_user)

@app.route('/logout', methods=["GET","POST"])
def logout():
    logout_user()
    return redirect(url_for("home"))
@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route('/form_entry', methods=["GET","POST"])
def form_entry():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("message")
        my_email = os.getenv("MY_EMAIL")

        try:
            connection = smtplib.SMTP("smtp.gmail.com", port=587, timeout=10)
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=my_email,
                msg=f"Subject: Message from Movie Corner Site: {name}\n\n"
                    f"Name: {name},\nEmail: {email},\nPhone: {phone},\nMessage: {message}"
            )
            connection.close()
            flash("Your message has been sent successfully!", "success")
            return render_template("contact.html", message_sent=True)

        except smtplib.SMTPException:
            app.logger.exception("Error while sending the email!")
            flash("Failed to send the message. Please try again later.", "danger")
            return render_template("contact.html", message_sent=False)

    return render_template("contact.html", message_sent=False)

    



if __name__ == "__main__":
    app.run(debug=True, port=5002)
