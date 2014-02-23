player = {
    defaults: {
        swfPath: "/js",
        supplied: "m4a, mp3, oga"
    },

    init: function(el, options, debug) {
        if (debug) options.solution = "flash, html";

        var opts = $.extend({}, this.defaults, options);

        this.playlist = new jPlayerPlaylist({
            jPlayer: el,
            cssSelectorAncestor: "#jp_container_1"
        }, [], opts);

        return this;
    },

    /*
    play the songs in a queue given by songs
     @param songs - an array of song objects having structure:
     {
     title: '',
     artist: '',
     mp3: '',
     poster: ''
     }
    */
    playSongs: function(songs) {
        this.playlist.setPlaylist(songs);
        this.playlist.play(0);
    },


    /*
    add a song to this player's playlist
    @param song - the song to add (has same structure as a single song in playSongs above)
    @param playNow - if true, play the song when its added
     */
    addSong: function(song, playNow) {
        this.playlist.add(song, playNow);
    }
};
