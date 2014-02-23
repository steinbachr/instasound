import requests
import json
import logging
import pdb

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


class Mix():
    """
    This class represents an 8Tracks Mix
    """
    def __init__(self, id, name, description, tags):
        self.id = id
        self.name = name
        self.description = description
        self.tags = tags

    def __unicode__(self):
        return '{name} - {description} ||| {tags}'.format(name=self.name, description=self.description, tags=self.tags)


class MixSet():
    """
    This class provides methods for playback an 8tracks Mix
    """
    def __init__(self, mix, headers, play_token):
        self.mix = mix
        self.headers = headers
        self.play_token = play_token

        self.started_playing = False
        self.play_url = 'http://8tracks.com/sets/{token}/play.json?mix_id={mix_id}'.format(token=play_token, mix_id=mix.id)
        self.next_url = 'http://8tracks.com/sets/{token}/next.json?mix_id={mix_id}'.format(token=play_token, mix_id=mix.id)
        self.skip_url = 'http://8tracks.com/sets/{token}/skip.json?mix_id={mix_id}'.format(token=play_token, mix_id=mix.id)

    def get_stream_data(self):
        """
        get the data for streaming this Set's mix
        @return dictionary containing track information, url, and whether skipping is allowed
        """
        logging.info('getting play url {url} now...'.format(url=self.play_url if not self.started_playing else self.next_url))
        response = requests.get(self.play_url if not self.started_playing else self.next_url, headers=self.headers)
        self.started_playing = True
        parsed = response.json()
        mix_set = parsed['set']
        track = mix_set['track']

        result = {
            'id': track['id'],
            'stream_url': track['track_file_stream_url'],
            'name': track['name'],
            'performer': track['performer'],
            'skip_allowed': mix_set['skip_allowed'],
            'done': mix_set['at_last_track']
        }
        logging.info('result is {result}'.format(result=result))

        return result


class Api():	
    """
    all external interaction comes through this class
    """
    def __init__(self, api_key=None):
        self.base_url = "http://8tracks.com/"
        self.mixes_url = lambda smart_id: "{base}mix_sets/{smart_id}.json?include=mixes+pagination".format(base=self.base_url, smart_id=smart_id)
        self.token_url = 'http://8tracks.com/sets/new.json'
        self.headers = {'X-Api-Key': api_key, 'X-Api-Version': 3}

        self.play_token = self.get_play_token()
        self.current_set = None


    def get_play_token(self):
        """
        get a play token so we can playback mixes. Note: There should never be a reason to call this externally
        @return the fetched play token
        """
        logging.info("getting a play token...")
        response = requests.get(self.token_url, headers=self.headers)
        response_json = response.json()
        token = response_json['play_token']
        logging.info("got play token {token}".format(token=token))
        return token


    #####-----< PUBLIC FUNCTIONS START HERE >-----#####

    ##--< Search Methods >--##

    def get_mixes(self, num_results=10, filter=None):
        """
        get a list of mixes from 8tracks
        @param num_results - the number of results to fetch. Defaults to 10. This should be an even number.
        @param filter - a tuple representing the smart id to use for filtering results.
        @return a list of Mix instances based on 8tracks results
        """
        logging.info("in get_mixes")
        request_url = '{base}&per_page={num_results}'.format(base=self.mixes_url(filter if filter else 'all'), num_results=num_results)
        logging.info("requesting url {url}".format(url=request_url))

        response = requests.get(request_url, headers=self.headers)
        response_json = response.json()

        mixes = response_json['mix_set']['mixes']
        logging.info("got mixes!")
        return [Mix(m['id'], m['name'], m['description'], m['tag_list_cache']) for m in mixes]


    def get_mixes_by_tag(self, tags, num_results=10):
        """
        get a list of  mixes having the given tags (separated by +)
        @param tag - the tag to filter mixes by
        @param num_results - the number of results to fetch
        @return a list of Mix instances based on 8tracks results
        """
        logging.info("getting mixes by tags having value {val}".format(val=tags))
        return self.get_mixes(num_results=num_results, filter='tags:{tags}'.format(tags=tags))

    def get_mixes_by_artist(self, artist, num_results=10):
        """
        get a list of  mixes featuring a given artist
        @param artist - the artist to filter mixes by
        @param num_results - the number of results to fetch
        @return a list of Mix instances based on 8tracks results
        """
        logging.info("getting mixes by artist having value {val}".format(val=artist))
        return self.get_mixes(num_results=num_results, filter='artist:{artist}'.format(artist=artist))

    def get_mixes_by_keyword(self, keyword, num_results=10):
        """
        get a list of  mixes containing a given keyword
        @param keyword - the keyword to filter mixes by
        @param num_results - the number of results to fetch
        @return a list of Mix instances based on 8tracks results
        """
        logging.info("getting mixes having keyword {val}".format(val=keyword))
        return self.get_mixes(num_results=num_results, filter='keyword:{keyword}'.format(keyword=keyword))

    ##--< Playback Methods >--##

    def start_playback(self, mix):
        """
        get the information for playing the given mix
        @param mix - the Mix instance to play
        @return a dictionary containing the  first track to be played in the mix as represented by
        a dictionary having keys: stream_url, name, performer, skip_allowed
        """
        logging.info("getting playback info for {mix}".format(mix=mix))
        self.current_set = MixSet(mix, self.headers, self.play_token)
        return self.current_set.get_stream_data()

    def next_song(self):
        """
        get the information for playing the next song in the current set
        @return same thing as start_playback except for the next track
        """
        logging.info("going to next song in the set")
        return self.current_set.get_stream_data()

    def report_song_play(self, track_id):
        """
        report the play of a song in the current mix
        @param track_id - the id of the track to report
        """
        report_url = 'http://8tracks.com/sets/{token}/report.json?track_id={track_id}&mix_id={mix_id}'.format(token=self.play_token,
                                                                                                              track_id=track_id,
                                                                                                              mix_id=self.current_set.mix.id)
        logging.info("reporting the track to url {url}".format(url=report_url))
        requests.post(report_url)


