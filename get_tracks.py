import soundcloud
import logging
from eight_py import Api
import pdb
import requests


EIGHT_TRACKS = "8Tracks"
SOUNDCLOUD = "Soundcloud"

SOUNDCLOUD_CLIENT_ID = '7d365fefd91122c615f4ebbe66f512b1'


class Controller():
    def __init__(self, eight_api):
        self.media_source = SOUNDCLOUD
        self.eight_api = eight_api
        self.soundcloud_api = soundcloud.Client(client_id=SOUNDCLOUD_CLIENT_ID)

        logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(message)s')

    def set_media_source(self, new_source):
        self.media_source = new_source

    def get_soundcloud_songs(self, filter_val=None):
        """
        get songs from soundcloud
        @param filter_val - if given, filter the songs by this term
        @return an array of track dictionaries containing url, title, and artist for the retrieved songs
        """
        logging.info('getting tracks from soundcloud')
        tracks = self.soundcloud_api.get('/tracks', q=filter_val, filter='streamable', limit=10) if filter_val else self.soundcloud_api.get('/tracks', filter='streamable', limit=20)
        normalized_tracks = []
        for track in tracks:
            if track.streamable:
                title = track.title.encode('utf-8')
                url_to_play = '{url}?consumer_key={key}'.format(url=track.stream_url, key=SOUNDCLOUD_CLIENT_ID)
                logging.info('adding streamable url for track {name} with url {url}'.format(name=track.title.encode('utf-8'),  url=track.stream_url.encode('utf-8')))

                normalized_tracks.append({
                    'mp3': url_to_play,
                    'title': title,
                    'artist': 'soundcloud',
                    'poster': track.artwork_url,
                    'downloadUrl': track.download_url if track.downloadable else ''
                })
            
        return normalized_tracks

    def get_8tracks_song(self, filter_type=None, filter_val=None, starting_playback=True):
        """
        get a song from 8tracks (since we cant just get a bunch of songs at once like we can for soundcloud)
        @param filter_type - the type of filter to apply (keyword, artist, tag)
        @param filter_val - the value to filter song results by
        @param starting_playback - if true, it means that we're starting playback of a mix, false means were going to next
                    track in the mix.
        @return a track to stream (unless no mixes exist with the given filters, in which case we return None)
        """
        logging.info('getting tracks from 8tracks')

        if starting_playback:
            #if there's a type, there's a value
            if filter_type:
                if filter_type.lower() == 'keyword':
                    mixes = self.eight_api.get_mixes_by_keyword(filter_val, num_results=1)
                elif filter_type.lower() == 'artist':
                    mixes = self.eight_api.get_mixes_by_artist(filter_val, num_results=1)
                else:
                    mixes = self.eight_api.get_mixes_by_tag(filter_val, num_results=1)
            else:
                mixes = self.eight_api.get_mixes(num_results=1)

            if mixes:
                track = self.eight_api.start_playback(mixes[0])
            else:
                return None
        else:
            track = self.eight_api.next_song()
            self.eight_api.report_song_play(track['id'])

        while not track:
            track = self.eight_api.next_song()
        logging.info('got track {track}'.format(track=track))

        # try to get a version of the song for download from soundcloud
        download_url = ''
        soundcloud_matches = self.soundcloud_api.get('/tracks', q='{name} {artist}'.format(name=track['name'], artist=track['performer']),
                                                     filter='downloadable')
        for download_track in soundcloud_matches:
            if download_track.downloadable:
                download_url = download_track.download_url
                break

        return {
            'mp3': track['stream_url'],
            'title': track['name'],
            'artist': track['performer'],
            'poster': '',
            'downloadUrl': download_url
        }

    def download(self, download_url):
        """
        return a request object containing the data retrieved by accessing the download url for the track
        @param download_url - the url for downloading a track
        @return request response object
        """
        url = '{track_url}?client_id={c_id}'.format(track_url=download_url, c_id=SOUNDCLOUD_CLIENT_ID)
        return requests.get(url)