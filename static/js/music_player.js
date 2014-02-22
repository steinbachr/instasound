player = {
    defaults: {
        swfPath: "/js",
        supplied: "m4a, oga"
    },

    init: function(el, options, debug) {
        if (debug) options.solution = "flash, html";

        var opts = $.extend({}, this.defaults, options);
        this.jPlayer = $(el).jPlayer(opts).data().jPlayer;

        return this;
    },

    /*
    play the songs in a queue given by songs
     @param songs - an array of song urls
    */
    playSongs: function(songs) {
        this.jPlayer.setMedia({
            track: songs.map(function(s) {
                return {
                    src: s
                }
            })
        });
    }

};
