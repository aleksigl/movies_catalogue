from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'brace_for_impact'

movies = [
    {'id': 1, 'title': 'Movie 1', 'image': 'movie1.jpg'},
    {'id': 2, 'title': 'Movie 2', 'image': 'movie2.jpg'},
    {'id': 3, 'title': 'Movie 3', 'image': 'movie3.jpg'},
    {'id': 4, 'title': 'Movie 4', 'image': 'movie3.jpg'},
]


@app.route('/')
def homepage():
    return render_template("homepage.html", movies=movies)


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


if __name__ == '__main__':
    app.run(debug=True)
