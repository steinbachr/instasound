import soundcloud
import logging
from Tkinter import *
from PIL import Image, ImageTk
from lib import vlc
from eight_py import Api
import pdb


EIGHT_TRACKS = "8Tracks"
SOUNDCLOUD = "Soundcloud"

class Controller():
    def __init__(self):
        self.vlc = vlc.Instance()        
        self.media_player = self.vlc.media_list_player_new()   
        self.media = None     
        self.media_source = SOUNDCLOUD
        # string vars set by Window instance
        self.info_var = None
        self.filter_var = None

        logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(message)s')

    def set_media_source(self, new_source):
        self.media_source = new_source

    def add_track_info(self, track_name):
        """
        add a new track to this controller's string var which is displaying all song info
        """
        self.info_var.set('{prev} \n {cur}'.format(prev=self.info_var.get().encode('utf-8'), cur=track_name.encode('utf-8')))

    def get_soundcloud_songs(self):
        CLIENT_ID = '7d365fefd91122c615f4ebbe66f512b1'
        CLIENT_SECRET = 'cde1a5fde5cb20712dda2070f852d5dc'
        client = soundcloud.Client(client_id=CLIENT_ID)

        filter_val = self.filter_var.get()
        self.info_var.set('\n\n Now playing Soundcloud Songs: \n')
        
        logging.info('getting tracks from soundcloud')
        tracks = client.get('/tracks', q=filter_val, limit=10) if filter_val else client.get('/tracks', limit=20)
        urls = []        
        for track in tracks:
            if track.streamable:
                logging.info('adding streamable url for track {name} with url {url}'.format(name=track.title.encode('utf-8'),  url=track.stream_url.encode('utf-8')))
                url_to_play = '{url}?consumer_key={key}'.format(url=track.stream_url, key=CLIENT_ID)
                self.add_track_info(track.title)
                urls.append(url_to_play)
            
        return urls

    def get_8tracks_songs(self):   
        """
        get a song from 8tracks (since we cant just get a bunch of songs at once like we can for soundcloud)
        @return a list of song urls to stream
        """
        logging.info('getting tracks from 8tracks')
        API_KEY = '7fe2e057bb81abf2248a06ecab027b8dc09e01d3'        
        self.info_var.set('\n\n Now playing 8Tracks Songs: \n')
        filter_val = self.filter_var.get()

        api = Api(api_key=API_KEY)
        mixes = api.get_mixes_by_keyword(filter_val, num_results=1) if filter_val else api.get_mixes(num_results=1)
        track = api.start_playback(mixes[0])        

        urls = []
        while not track['done']:
            urls.append(track['stream_url'])
            self.add_track_info('{name} by {performer}'.format(name=track['name'], performer=track['performer']))
            track = api.next_song()
            # if we were unable to fetch the track, re-query the api till we get one
            if not track:
                while not track:
                    track = api.next_song()
        logging.info('got track {track}'.format(track=track))

        return urls 

    def play_songs(self):        
        logging.info('getting song urls to play the tracks')
        song_urls = self.get_soundcloud_songs() if self.media_source == SOUNDCLOUD else self.get_8tracks_songs()

        if self.media:
            logging.info('there was already media, releasing it and stopping the playlist so we can load the new media')
            self.media.release()
            self.stop()

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

    def download(self):
        pass


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

        ##--< Labels >--##
        info_string_var = StringVar()
        info_label = Label(bottom_frame, textvariable=info_string_var)
        info_label.pack(side=LEFT)
        self.controller.info_var = info_string_var

        ##--< Radio Buttons >--##    
        eight_raw_image = Image.open("media/8tracks.jpg")    
        eight_raw_image = eight_raw_image.resize((100, 100), Image.ANTIALIAS)
        eight_image = ImageTk.PhotoImage(eight_raw_image)
        eight_button = Radiobutton(top_frame, image=eight_image, command=lambda: self.controller.set_media_source(EIGHT_TRACKS))
        eight_button.image = eight_image
        eight_button.grid(row=0, column=0)

        soundcloud_raw_image = Image.open("media/soundcloud.jpg")
        soundcloud_raw_image = soundcloud_raw_image.resize((100, 100), Image.ANTIALIAS)
        soundcloud_image = ImageTk.PhotoImage(soundcloud_raw_image)
        soundcloud_button = Radiobutton(top_frame, image=soundcloud_image, command=lambda: self.controller.set_media_source(SOUNDCLOUD))
        soundcloud_button.image = soundcloud_image
        soundcloud_button.grid(row=0, column=1)
        ##--< Buttons >--##
        play_button = Button(top_frame, text="Play", command=lambda: self.controller.play_songs())
        play_button.grid(row=1, column=0)

        pause_button = Button(top_frame, text="Pause", command=self.controller.pause)
        pause_button.grid(row=1, column=1)

        previous_button = Button(top_frame, text="Previous", command=self.controller.previous)
        previous_button.grid(row=1, column=2)

        next_button = Button(top_frame, text="Next", command=self.controller.next)
        next_button.grid(row=1, column=3)

        filter_type = Radiobutton(top_frame)
        filter_type.grid(row=2, column=2)
        filter_type.grid_forget()

        filter_string_var = StringVar()
        filter_button = Button(top_frame, text="Filter", command=lambda: self.controller.play_songs())
        filter_button.grid(row=2, column=0)
        self.controller.filter_var = filter_string_var

        ##--< Entries >--##
        filter_entry = Entry(top_frame, bd=5, textvariable=filter_string_var)
        filter_entry.grid(row=2, column=1)


Window()