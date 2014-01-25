import soundcloud
from lib import vlc

class Controller():
    def __init__(self):
        self.vlc = vlc.Instance()

    def get_songs(self):
        CLIENT_ID = '7d365fefd91122c615f4ebbe66f512b1'
        CLIENT_SECRET = 'cde1a5fde5cb20712dda2070f852d5dc'
        client = soundcloud.Client(client_id=CLIENT_ID)
        
        tracks = client.get('/tracks', limit=10)
        urls = []
        for track in tracks:
            url_to_play = '{url}?consumer_key={key}'.format(url=track.stream_url, key=CLIENT_ID)
            urls.append(url_to_play)
            print url_to_play
            
        return urls
              
    def play_songs(self, song_urls):
        media_list = self.vlc.media_list_new(mrls=song_urls)
        media_player = self.vlc.media_list_player_new()
        media_player.set_media_list(media_list)
        media_player.play()
   

controller = Controller()
controller.play_songs(controller.get_songs())