from flask import render_template, flash, current_app
import requests
from bs4 import BeautifulSoup

from . import main_bp

@main_bp.route("/", methods=["GET", "POST"])
def home():
    images, titles, article_link = [], [], []
    try:
        response = requests.get(
            current_app.config["NEWS_URL"],
            headers=current_app.config["HTTP_HEADER"],
            timeout=8,
        )
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        article = soup.find_all(name="a", class_="bc-title-link")
        img = soup.find_all(name="a", class_="bc-img-link")

        if article:
            images = [src.get("srcset") for src in soup.select("picture source")[3::4]]
            titles = [x.get("title") for x in article]
            article_link = [y.get("href") for y in img]
    except requests.RequestException as e:
        current_app.logger.exception("Cannot download the News! %s", e)
        flash(" Cannot download the News!", "danger")

    return render_template("home.html", images=images, titles=titles, article_link=article_link)


@main_bp.route("/newmovies", methods=["GET", "POST"])
def new_movies():
    params = {
        "page": 1,
        "sort_by": "popularity.desc",
        "language": "en-US",
        "include_adult": False,
        "include_video": False,
    }
    url = "https://api.themoviedb.org/3/discover/movie"
    try:
        response = requests.get(
            url,
            headers={"accept": "application/json", "Authorization": current_app.config["TMDB_BEARER"]},
            params=params,
            timeout=8,
        )
        response.raise_for_status()
        results = response.json().get("results", [])
    except requests.RequestException as e:
        current_app.logger.exception("Cannot download the Movie list! %s", e)
        flash(" Cannot download the Movie list! ", "danger")
        results = []

    img_url = [x.get("backdrop_path") for x in results]
    title = [x.get("title") for x in results]
    year = [x.get("release_date") for x in results]
    descript = [x.get("overview") for x in results]
    return render_template("newmovies.html", title=title, year=year, descript=descript, img_url=img_url)


@main_bp.route("/new_tv", methods=["GET", "POST"])
def new_tv():
    params = {
        "page": 1,
        "sort_by": "popularity.desc",
        "language": "en-US",
        "include_adult": False,
        "include_video": False,
    }
    url = "https://api.themoviedb.org/3/discover/tv"
    try:
        response = requests.get(
            url,
            headers={"accept": "application/json", "Authorization": current_app.config["TMDB_BEARER"]},
            params=params,
            timeout=8,
        )
        response.raise_for_status()
        results = response.json().get("results", [])
    except requests.RequestException as e:
        current_app.logger.exception("Cannot download list of TV Series! %s", e)
        flash(" Cannot download list of  TV Series! ", "danger")
        results = []

    img_url = [x.get("backdrop_path") for x in results]
    title = [x.get("name") for x in results]
    year = [x.get("first_air_date") for x in results]
    descript = [x.get("overview") for x in results]
    return render_template("new-tv.html", title=title, year=year, descript=descript, img_url=img_url)


@main_bp.route("/contact")
def contact():
    return render_template("contact.html")


@main_bp.route("/form_entry", methods=["GET", "POST"])
def form_entry():
    from flask import request
    import smtplib

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("message")
        my_email = current_app.config["MY_EMAIL"]
        password = current_app.config["PASSWORD"]

        try:
            connection = smtplib.SMTP("smtp.gmail.com", port=587, timeout=10)
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=my_email,
                msg=(
                    f"Subject: Message from Movie Corner Site: {name}\n\n"
                    f"Name: {name},\nEmail: {email},\nPhone: {phone},\nMessage: {message}"
                ),
            )
            connection.close()
            flash("Your message has been sent successfully!", "success")
            return render_template("contact.html", message_sent=True)
        except smtplib.SMTPException as e:
            current_app.logger.exception("Error while sending the email! %s", e)
            flash("Failed to send the message. Please try again later.", "danger")
            return render_template("contact.html", message_sent=False)

    return render_template("contact.html", message_sent=False)
