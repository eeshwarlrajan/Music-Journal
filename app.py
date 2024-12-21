import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, get_flashed_messages, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from helpers import login_required
import requests
import hashlib

#Parts of code logicd and debugging guided by ChatGPT-4o/4o-mini

app = Flask(__name__)
app.secret_key = os.urandom(24)

db = SQL("sqlite:///musicjournal.db")

API_KEY = '8030e069aaa1ac5ddf79249c8ee62f02'

@app.route("/")
@login_required
def index():
    """ display albums in library"""
    albums = db.execute("SELECT * FROM library WHERE user_id = ?", session["user_id"])
    return render_template("library.html", albums=albums)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return render_template("input_error.html")

        if not password:
            return render_template("input_error.html")


        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return render_template("input_error.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """ register user """
    if request.method == "POST":
        if not request.form.get("username"):
            return render_template("input-error.html")
        elif not request.form.get("password"):
            return render_template("input_error.html")
        elif request.form.get("confirm_password") != request.form.get("password"):
            return render_template("confirmation_error.html")

        username = request.form.get("username")
        password = request.form.get("password")

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        #check if username already exists
        if len(rows) > 0:
            flash("Username Taken, Please use another one.", "error")
            return redirect("/register")

        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, generate_password_hash(password))

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        session["user_id"] = rows[0]["id"]

        flash("Registration Successful", "success")
        return redirect("/login")

    else:

        return render_template("register.html")

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    """ search for albums """
    if request.method == "POST":
        query = request.form.get("query")

        if not query:
            return jsonify({"error": "no search term provided"}), 400

        response = requests.get('http://ws.audioscrobbler.com/2.0/', {
            'method': 'album.search',
            'album': query,
            'api_key': API_KEY,
            'format': 'json' })

        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch data from API"}), 500

        data = response.json()
        albums = data.get('results', {}).get('albummatches', {}).get('album', [])
        return render_template('search_results.html', albums=albums)

    else:

        return render_template('search.html')


@app.route("/add", methods=["POST"])
@login_required
def add():
    """Add album to library"""
    album_name = request.form.get('album_name')
    artist_name = request.form.get('artist_name')
    album_image = request.form.get('album_image')

    response = requests.get('http://ws.audioscrobbler.com/2.0/', {
        'method': 'album.getInfo',
        'artist': artist_name,
        'album' : album_name,
        'api_key': API_KEY,
        'format': 'json' })

    if response.status_code != 200:
                return jsonify({"error": "Failed to fetch data from API"}), 500

    data = response.json()
    album = data.get('album', {})

    if not album:
        return jsonify({"error": "Album data not found in the response"}), 400

    album_id = album.get('id')

    if not album_id:
        unique_key = f"{album.get('name', '')}_{album.get('artist', '')}"
        album_id = hashlib.md5(unique_key.encode()).hexdigest()

    release_year = album.get('releasedate', 'Unknown').split(',')[0]
    album_cover_url = album.get('image', [{}])[3].get('#text')

    exists = db.execute("SELECT * FROM library WHERE user_id = ? AND id = ?", session["user_id"], album_id)
    if exists:
        flash("Album already added to library", "success")
        return redirect("/")

    db.execute("INSERT INTO library (id, user_id, album_name, artist_name, release_year, album_cover_url) VALUES (?, ?, ?, ? ,? ,?)",
               album_id, session["user_id"], album_name, artist_name, release_year, album_cover_url)

    return render_template('added.html', album=album)

@app.route("/review/<album_id>")
@login_required
def review(album_id):
    """Display and manage album reviews"""
    album = db.execute("SELECT * FROM library WHERE user_id = ? AND id = ?", session["user_id"], album_id)

    if not album:
        flash("Album not found in library, please add again", "danger")
        return redirect("/")

    album = album[0]
    return render_template("review.html", album=album)

@app.route("/submit_review/<album_id>", methods=["POST"])
@login_required
def submit_review(album_id):
    if not request.form.get("review"):
        flash("Please add review text", "success")
        return redirect(f"/review/{album_id}")
    if not request.form.get("rating"):
        flash("Please add rating", "success")
        return redirect(f"/review/{album_id}")

    review = request.form.get("review")
    rating = request.form.get("rating")

    db.execute("UPDATE library SET review = ?, rating = ? WHERE user_id = ? AND id = ?",
        review, rating, session["user_id"], album_id)

    flash("Review saved successfully!", "success")
    return redirect("/")

@app.route("/remove/<album_id>", methods=["POST"])
@login_required
def remove(album_id):
    if db.execute("DELETE FROM library WHERE id = ? AND user_id = ?;", album_id, session["user_id"]):
        flash("album removed successfuly", "success")
        return redirect("/")
    flash("album does not exist", "success")
    return redirect("/")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
