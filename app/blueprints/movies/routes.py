from flask import render_template, redirect, url_for, flash, request, session as flask_session, current_app
from flask_login import login_required, current_user
from werkzeug.exceptions import abort
import requests

from ...extensions import db
from ...models import Movies
from ...forms import EditForm, DeleteForm, AddForm

from . import movies_bp

@movies_bp.route("/movie_rank", methods=["GET", "POST"])
@login_required
def movie_rank():
    delete_form = DeleteForm()
    all_movies = (
        db.session.execute(db.select(Movies).where(Movies.user_id == current_user.id))
        .scalars()
        .all()
    )
    all_movies.sort(key=lambda m: (m.rating or 0), reverse=True)
    for i, movie in enumerate(all_movies, start=1):
        movie.ranking = i
    db.session.commit()
    return render_template("movie_rank.html", movies=all_movies, delete_form=delete_form)

@movies_bp.route("/add", methods=["GET", "POST"])
@login_required
def add():
    form = AddForm()
    if form.validate_on_submit():
        add_movie = form.add.data
        url = f"https://api.themoviedb.org/3/search/movie?query={add_movie}&include_adult=false&language=en-US&page=1"
        response = requests.get(
            url,
            headers={"accept": "application/json", "Authorization": current_app.config["TMDB_BEARER"]},
            timeout=8,
        )
        data = response.json().get("results", [])
        flask_session["new_record"] = [
            {
                "id": m.get("id"),
                "title": m.get("title"),
                "release_date": m.get("release_date"),
                "overview": m.get("overview"),
                "backdrop_path": m.get("backdrop_path"),
            }
            for m in data
        ]
        return redirect(url_for("movies.select"))
    return render_template("add.html", form=form)

@movies_bp.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    form = EditForm()
    movie_id = request.form.get("movie_id") or request.args.get("movie_id")
    movie = db.session.execute(db.select(Movies).filter_by(id=movie_id)).scalar_one_or_none()
    if form.validate_on_submit() and movie:
        movie.rating = float(form.rating.data)
        movie.review = form.review.data
        db.session.commit()
        return redirect(url_for("movies.movie_rank", movie_name=movie.title))
    return render_template("edit.html", form=form, name=movie)

@movies_bp.route("/delete", methods=["POST"])
@login_required
def delete():
    form = DeleteForm()
    movie_id = request.form.get("movie_id") or request.args.get("movie_id")
    movie = db.session.execute(db.select(Movies).filter_by(id=movie_id)).scalar_one_or_none()
    if form.validate_on_submit() and movie:
        db.session.delete(movie)
        db.session.commit()
    return redirect(url_for("movies.movie_rank"))

@movies_bp.route("/select", methods=["GET", "POST"])
@login_required
def select():
    result = flask_session.get("new_record") or []
    if not result:
        flash("No results! ", "warning")
        return redirect(url_for("movies.add"))

    how_many = len(result)
    movie_id = request.form.get("movie_id") or request.args.get("movie_id")

    if movie_id:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
        try:
            response = requests.get(
                url,
                headers={"accept": "application/json", "Authorization": current_app.config["TMDB_BEARER"]},
                timeout=8,
            )
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            current_app.logger.exception("We cannot download movie details! %s", e)
            flash(" We cannot download movie details! ", "danger")
            return redirect(url_for("movies.select"))

        img_path = data.get("backdrop_path")
        img_url = f"https://image.tmdb.org/t/p/w500/{img_path}" if img_path else None
        title = data.get("title")
        year = (data.get("release_date") or "")[:4]
        descript = data.get("overview")

        movie = Movies(
            title=title,
            year=int(year) if year.isdigit() else None,
            description=descript,
            rating=0,
            img_url=img_url,
            user_id=current_user.id,
        )
        db.session.add(movie)
        db.session.commit()
        return redirect(url_for("movies.movie_rank"))

    return render_template("select.html", result=result, how_many=how_many)
