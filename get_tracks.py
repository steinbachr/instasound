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
        song_info = kwargs.get('info')
        song_info.set('\n\n Now playing: \n')
        
        logging.info('getting tracks from soundcloud')
        tracks = client.get('/tracks', q=filter_val, limit=10) if filter_val else client.get('/tracks', limit=20)
        urls = []        
        for track in tracks:
            if track.streamable:
                logging.info('adding streamable url for track {name} with url {url}'.format(name=track.title.encode('utf-8'),  url=track.stream_url.encode('utf-8')))
                url_to_play = '{url}?consumer_key={key}'.format(url=track.stream_url, key=CLIENT_ID)
                song_info.set('{prev} \n {cur}'.format(prev=song_info.get().encode('utf-8'), cur=track.title.encode('utf-8')))
            urls.append(url_to_play)
            
        return urls

    def get_8tracks_songs(self):
        API_KEY = '7fe2e057bb81abf2248a06ecab027b8dc09e01d3.'

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

    def filter_songs(self, filter_val, info_var):
        logging.info('going to filter songs now')
        song_urls = self.get_songs(q=filter_val, info=info_var)
        self.stop()
        self.play_songs(song_urls)

    def download(self):
        pass



class Window():
    def __init__(self):
        self.controller = Controller()

        top = Tk() 
        self.setup_widgets(top)       
        top.mainloop() 

    def setup_widgets(self, window):        
        ##--< Labels >--##
        info_string_var = StringVar()
        info_label = Label(window, textvariable=info_string_var)
        info_label.grid(row=2, column=2)

        ##--< Buttons >--##
        play_button = Button(window, text="Play", command=lambda: self.controller.play_songs(self.controller.get_songs(info=info_string_var)))
        play_button.grid(row=0, column=0)

        pause_button = Button(window, text="Pause", command=self.controller.pause)
        pause_button.grid(row=0, column=1)

        previous_button = Button(window, text="Previous", command=self.controller.previous)
        previous_button.grid(row=0, column=2)

        next_button = Button(window, text="Next", command=self.controller.next)
        next_button.grid(row=0, column=3)

        filter_string_var = StringVar()
        filter_button = Button(window, text="Filter", command=lambda: self.controller.filter_songs(filter_string_var.get(), info_string_var))
        filter_button.grid(row=1, column=0)

        ##--< Entries >--##
        filter_entry = Entry(window, bd=5, textvariable=filter_string_var)
        filter_entry.grid(row=1, column=1)


Window()