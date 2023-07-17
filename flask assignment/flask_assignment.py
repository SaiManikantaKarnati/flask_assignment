from flask import Flask, render_template, jsonify, request
import urllib.request, json
import os
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

user_data = {
    "admin": "password",
    "admin1": "password"
}

@auth.verify_password
def verify(username, pwd):
    if not(username and pwd):
        return False
    return user_data.get(username) == pwd

@app.route("/")
@auth.login_required
def get_movies():
    url = "https://api.themoviedb.org/3/discover/movie?api_key=78a5ffaa7ce2c9e99067bfe14119748a"

    response = urllib.request.urlopen(url)
    data = response.read()
    movie_dict = json.loads(data)

    return movie_dict.get("results", [])

@app.route("/movies")
def get_movies_html():
    url = "https://api.themoviedb.org/3/discover/movie?api_key=78a5ffaa7ce2c9e99067bfe14119748a"

    response = urllib.request.urlopen(url)
    data = response.read()
    movie_dict = json.loads(data)

    return render_template("index.html", movies=movie_dict["results"])

@app.route("/movie/<name>")
def get_movie_by_name(name=None):
    if name:
        query_name = urllib.parse.quote_plus(name)
        url = f"https://api.themoviedb.org/3/search/movie?api_key=78a5ffaa7ce2c9e99067bfe14119748a&query={query_name}"
        response = urllib.request.urlopen(url)
        data = response.read()
        movie_dict = json.loads(data)

        if movie_dict.get("total_results", 0) > 0:
            movie = movie_dict.get("results", [])[0]
            return render_template("movie_details.html", movie=movie)
        else:
            return "Movie not found."

    return get_movies()

@app.route("/api/movies")
def get_movies_json():
    movies = get_movies()
    filtered_movies = []
    for movie in movies:
        filtered_movie = {
            "original_title": movie.get("original_title"),
            "original_language": movie.get("original_language"),
            "release_date": movie.get("release_date"),
            "overview": movie.get("overview"),
            "backdrop_path": movie.get("backdrop_path")
        }
        filtered_movies.append(filtered_movie)

    return jsonify(filtered_movies)

@app.route("/api/movie/<name>")
def get_movie_by_name_json(name=None):
    if name:
        query_name = urllib.parse.quote_plus(name)
        url = f"https://api.themoviedb.org/3/search/movie?api_key=78a5ffaa7ce2c9e99067bfe14119748a&query={query_name}"
        response = urllib.request.urlopen(url)
        data = response.read()
        movie_dict = json.loads(data)

        if movie_dict.get("total_results", 0) > 0:
            movie = movie_dict.get("results", [])[0]
            filtered_movie = {
            "original_title": movie.get("original_title"),
            "original_language": movie.get("original_language"),
            "release_date": movie.get("release_date"),
            "overview": movie.get("overview"),
            "backdrop_path": movie.get("backdrop_path")
            }
            return jsonify(filtered_movie)
        else:
            return jsonify({"error": "Movie not found."})

    # If no movie name provided, return details of all movies
    movies = get_movies()
    filtered_movies = []
    for movie in movies:
        filtered_movie = {
            "id": movie.get("id"),
            "original_title": movie.get("original_title"),
            "release_date": movie.get("release_date")
        }
        filtered_movies.append(filtered_movie)

    return jsonify(filtered_movies)

if __name__ == "__main__":
    app.run(debug=True)
