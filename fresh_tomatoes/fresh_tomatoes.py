import os
import yaml

from flask import Flask
from flask import g, render_template, redirect, request, url_for
from flask_bootstrap import Bootstrap

from . import db
from .youtube import YouTubeForm, get_youtube


def create_app():
    """Creates a Flask app."""
    app = Flask(__name__)

    # Load default config and override config from an environment variable
    app.config.update({
        'DATABASE': 'sqlite:////tmp/fresh_tomatoes.sqlite',
        'SECRET_KEY': 'secret',
        'USERNAME': 'admin',
        'PASSWORD': 'default',
    })
    app.config.from_envvar('FRESH_TOMATOES_SETTINGS', silent=True)

    # Enable Twitter Bootstrap integration
    Bootstrap(app)

    return app


app = create_app()


def load_sample_data():
    with app.open_resource('sample_data.yaml', 'r') as f:
        data = yaml.load(f.read())
    db.load_sample_data(app, g, data)


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    if app.debug:
        # Remove SQLite database during development.
        db_path = app.config['DATABASE']
        if db_path.startswith('sqlite:///'):
            db_path = db_path[10:]
            if os.path.exists(db_path):
                os.remove(db_path)

    # Initialize the database.
    db.init(app, g)

    # Load sample data during development.
    if app.debug:
        load_sample_data()

    print('Initialized the database.')


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'db_engine'):
        g.db_engine.dispose()


@app.route('/')
def index():
    """Handles the landing page."""
    movies = db.list_movies(app, g)
    youtube_form = YouTubeForm()
    return render_template('index.html', movies=movies,
                           youtube_form=youtube_form)


@app.route('/add', methods=['POST'])
def add():
    """Handles adding a movie by YouTube URI."""
    form = YouTubeForm(request.form)
    if form.validate():
        data = get_youtube(form.uri)
        db.add_movie(app, g, title=data.title,
                     image_uri=data.image_uri,
                     embed_uri=data.embed_uri)
    return redirect(url_for('index'))


@app.route('/remove/<int:movie_id>', methods=['POST'])
def remove(movie_id):
    """Handles removing a movie by ID."""
    db.remove_movie(app, g, movie_id)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
