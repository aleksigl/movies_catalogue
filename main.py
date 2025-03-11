from flask import Flask, render_template, request, redirect, url_for, session, flash
import tmdb_client
import random

app = Flask(__name__)
app.secret_key = 'brace_for_impact'

movies = tmdb_client.get_movies()


@app.route('/')
def homepage():
    selected_list = request.args.get('list_type', 'popular')
    movies = tmdb_client.get_movies(list_name=selected_list)
    return render_template("homepage.html", movies=movies, current_list=selected_list)


@app.context_processor
def utility_processor():
    def tmdb_image_url(path, size):
        return tmdb_client.get_poster_url(path, size)
    return {"tmdb_image_url": tmdb_image_url}


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    return render_template('search.html', query=query, movies=movies)


@app.route('/favourites')
def favourites():
    favs = session.get('favourites', [])
    return render_template('favourites.html', favs=favs, movies=movies)


@app.route('/add_to_favourites/<int:movie_id>')
def add_to_favourites(movie_id):
    movie = next((m for m in movies if m['id'] == movie_id), None)
    if movie:
        favs = session.get('favourites', [])
        if movie_id not in favs:
            favs.append(movie_id)
        session['favourites'] = favs
    return redirect(url_for('homepage'))


@app.route('/remove_from_favourites/<int:movie_id>')
def remove_from_favourites(movie_id):
    favs = session.get('favourites', [])
    if movie_id in favs:
        favs.remove(movie_id)
    session['favourites'] = favs
    return redirect(url_for('favourites'))


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        flash('Wiadomość została wysłana. Skontaktujemy się z Tobą wkrótce!', 'success')
        return redirect(url_for('homepage'))
    return render_template('contact.html')


@app.route("/movie/<movie_id>")
def movie_details(movie_id):
    details = tmdb_client.get_single_movie(movie_id)
    cast = tmdb_client.get_single_movie_cast(movie_id)
    movie_images = tmdb_client.get_movie_images(movie_id)
    selected_backdrop = random.choice(movie_images['backdrops'])
    return render_template("movie_details.html", movie=details, cast=cast, selected_backdrop=selected_backdrop)


@app.context_processor
def poster_processor():
    def tmdb_large_poster_url(path, size):
        return tmdb_client.get_large_poster(path, size)
    return {"tmdb_large_poster_url": tmdb_large_poster_url}


@app.route("/movie/<movie_id>")
def movie_cast(movie_id):
    details = tmdb_client.get_single_movie(movie_id)
    cast = tmdb_client.get_single_movie_cast(movie_id)
    return render_template("movie_details.html", movie=details, cast=cast)


if __name__ == '__main__':
    app.run(debug=True)
