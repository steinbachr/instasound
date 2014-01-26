import soundcloud
import logging
from Tkinter import *
from lib import vlc
import pdb


class Controller():
    def __init__(self):
        self.vlc = vlc.Instance()
        self.media_player = self.vlc.media_list_player_new()   
        self.media = None     

        logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(message)s')

    def get_songs(self, **kwargs):
        CLIENT_ID = '7d365fefd91122c615f4ebbe66f512b1'
        CLIENT_SECRET = 'cde1a5fde5cb20712dda2070f852d5dc'
        client = soundcloud.Client(client_id=CLIENT_ID)
        filter_val = kwargs.get('q', None)
        
        logging.info('getting tracks from soundcloud')
        tracks = client.get('/tracks', q=filter_val, limit=10) if filter_val else client.get('/tracks', limit=20)
        urls = []        
        for track in tracks:
            if track.streamable:
                logging.info('adding track {name} with url {url}'.format(name=track.title.encode('utf-8'),  url=track.stream_url.encode('utf-8')))
                url_to_play = '{url}?consumer_key={key}'.format(url=track.stream_url, key=CLIENT_ID)
                urls.append(url_to_play)
            
        return urls

    def play_songs(self, song_urls):
        logging.info('getting ready to play the tracks')
        if self.media:
            self.media.release()
        self.media = self.vlc.media_list_new(mrls=song_urls)        

        self.media_player.set_media_list(self.media)
        self.media_player.play()
        logging.info('now playing')

    def pause(self):
        logging.info('pausing playback')
        self.media_player.pause()

    def stop(self):
        logging.info('stopping playback')
        self.media_player.stop()

    def next(self):
        logging.info('going to next track')
        self.media_player.next()

    def previous(self):
        logging.info('going to next track')
        self.media_player.previous()

    def filter_songs(self, filter_val):
        logging.info('going to filter songs now')
        song_urls = self.get_songs(q=filter_val)
        self.stop()
        self.play_songs(song_urls)



class Window():
    def __init__(self):
        self.controller = Controller()

        top = Tk() 
        self.setup_widgets(top)       
        top.mainloop() 

    def setup_widgets(self, window):
        ##--< Frames >--##
        top_frame = Frame(window)
        top_frame.pack(side=TOP)

        bottom_frame = Frame(window)
        bottom_frame.pack(side=BOTTOM)

        filter_frame = Frame(bottom_frame)
        filter_frame.pack(side=BOTTOM)

        ##--< Buttons >--##
        play_button = Button(top_frame, text="Play", command=lambda: self.controller.play_songs(self.controller.get_songs()))
        play_button.pack(side=LEFT)

        pause_button = Button(top_frame, text="Pause", command=self.controller.pause)
        pause_button.pack(side=LEFT)

        next_button = Button(bottom_frame, text="Next", command=self.controller.next)
        next_button.pack(side=LEFT)

        previous_button = Button(bottom_frame, text="Previous", command=self.controller.previous)
        previous_button.pack(side=LEFT)

        v = StringVar()
        filter_button = Button(bottom_frame, text="Filter", command=lambda: self.controller.filter_songs(v.get()))
        filter_button.pack(side=RIGHT)

        ##--< Labels >--##
        filter_label = Label(filter_frame, text="Filter Songs")
        filter_label.pack(side=LEFT)

        ##--< Entries >--##
        filter_entry = Entry(filter_frame, bd=5, textvariable=v)
        filter_entry.pack(side=LEFT)


Window()