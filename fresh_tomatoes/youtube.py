import requests

from collections import namedtuple
from html.parser import HTMLParser

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

YouTubeFilm = namedtuple('YouTubeFilm', ['title', 'embed_uri', 'image_uri'])


class YouTubeParser(HTMLParser):
    """Parses a YouTube page to extract the title and useful URLs."""

    def __init__(self, *args, **kwargs):
        super(YouTubeParser, self).__init__(*args, **kwargs)
        self.video_id = None
        self.title = None
        self.embed_uri = None
        self.image_uri = None

    def handle_starttag(self, tag, attrs):
        # Turn attrs into dictionary.
        attrs = dict(attrs)

        # Check only at meta tags.
        if tag != 'meta':
            return

        # Extract video ID.
        if attrs.get('itemprop') == 'videoId':
            self.video_id = attrs.get('content', self.video_id)
            return

        # Extract title.
        if attrs.get('name') == 'title':
            self.title = attrs.get('content', self.title)
            return

        # Extract image and embed URLs.
        value = attrs.get('content')
        if value:
            prop = attrs.get('property')
            if prop == 'og:image':
                self.image_uri = value
            elif prop == 'og:video:url':
                if 'embed' in value:
                    self.embed_uri = value


def get_youtube(uri):
    """Fetches and parses a YouTube URI to extract film information."""
    resp = requests.get('https://www.youtube.com/watch?v=Usz-0dvT4k4')

    # Parse YouTube HTML.
    parser = YouTubeParser()
    parser.feed(resp.text)

    # Check if poster image exists.
    if parser.video_id:
        poster_uri = '//i.ytimg.com/vi/%s/movieposter.jpg' % parser.video_id
        if poster_uri in resp.text:
            parser.image_uri = 'https://%s' % poster_uri

    return YouTubeFilm(parser.title, parser.embed_uri, parser.image_uri)


class YouTubeForm(FlaskForm):
    """Form for submitting a YouTube URI."""
    uri = StringField('YouTube URL', validators=[DataRequired()])
    submit = SubmitField('Add Film')
