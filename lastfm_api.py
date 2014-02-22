import pylast


class LastFmApi():
    def __init__(self, username='steinbachrj', password='leonhall'):
        self.api_key = 'eb0ce903d873881d016c51d53b2be740'
        self.secret = 'bdd6db6d7ac37de07b8f34877b88dad9'
        self.handle = pylast.LastFMNetwork(api_key=self.api_key, api_secret=self.secret,
                                           username=username, password_hash=pylast.md5(password))