import soundcloud

def get_songs():
    CLIENT_ID = '7d365fefd91122c615f4ebbe66f512b1'
    CLIENT_SECRET = 'cde1a5fde5cb20712dda2070f852d5dc'
    client = soundcloud.Client(client_id=CLIENT_ID)
    
    tracks = client.get('/tracks', limit=10)
    for track in tracks:
        print track.stream_url
        
def play_songs(songs):
    pass

songs = get_songs()
play_songs(songs)