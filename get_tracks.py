import soundcloud
import logging
from eight_py import Api
import pdb


EIGHT_TRACKS = "8Tracks"
SOUNDCLOUD = "Soundcloud"


class Controller():
    def __init__(self):
        self.media_source = SOUNDCLOUD
        logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(message)s')

    def set_media_source(self, new_source):
        self.media_source = new_source

    def get_soundcloud_songs(self, filter_val=None):
        """
        get songs from soundcloud
        @param filter_val - if given, filter the songs by this term
        @return an array of track dictionaries containing url, title, and artist for the retrieved songs
        """
        CLIENT_ID = '7d365fefd91122c615f4ebbe66f512b1'
        client = soundcloud.Client(client_id=CLIENT_ID)

        logging.info('getting tracks from soundcloud')
        tracks = client.get('/tracks', q=filter_val, filter='streamable', limit=10) if filter_val else client.get('/tracks', filter='streamable', limit=20)
        normalized_tracks = []
        for track in tracks:
            if track.streamable:
                title = track.title.encode('utf-8')
                url_to_play = '{url}?consumer_key={key}'.format(url=track.stream_url, key=CLIENT_ID)
                logging.info('adding streamable url for track {name} with url {url}'.format(name=track.title.encode('utf-8'),  url=track.stream_url.encode('utf-8')))

                normalized_tracks.append({
                    'mp3': url_to_play,
                    'title': title,
                    'artist': 'soundcloud',
                    'poster': track.artwork_url
                })
            
        return normalized_tracks

    def get_8tracks_songs(self, filter_val=None):
        """
        get a song from 8tracks (since we cant just get a bunch of songs at once like we can for soundcloud)
        @param filter_val - the value to filter song results by
        @return a list of song urls to stream
        """
        logging.info('getting tracks from 8tracks')
        API_KEY = '7fe2e057bb81abf2248a06ecab027b8dc09e01d3'        

        api = Api(api_key=API_KEY)
        mixes = api.get_mixes_by_keyword(filter_val, num_results=1) if filter_val else api.get_mixes(num_results=1)
        track = api.start_playback(mixes[0])        

        urls = []
        while not track['done']:
            urls.append(track['stream_url'])
            track = api.next_song()
            # if we were unable to fetch the track, re-query the api till we get one
            if not track:
                while not track:
                    track = api.next_song()
        logging.info('got track {track}'.format(track=track))

        return urls

    def next(self):
        logging.info('going to next track')
        self.media_player.next()

    def previous(self):
        logging.info('going to next track')
        self.media_player.previous()

    def download(self):
        pass