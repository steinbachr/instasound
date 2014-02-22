var page = {
    soundcloudUrl: '/play-soundcloud',
    mediaSource: 'soundcloud',

    init: function() {
        player.init("#jquery_jplayer_1", {}, false);

        this.playSoundcloud();
        this.clickBindings();
    },

    clickBindings: function() {
        var _this = this;

        /* click bindings */
        $('.nav_item').click(function() {
            $('.nav_item').removeClass('selected');
            $(this).addClass('selected');
            this.mediaSource = $(this).data('mediaSource');
        });

        $('.apply_filters').click(function() {
            var filterVal = $(this).closest('.filters').find('input').val();
            _this.playSoundcloud(filterVal);
        });
    },

    /*
    play songs from soundcloud
    @param filtVal - if provided, this is the filter
     */
    playSoundcloud: function(filtVal) {
        var query = filtVal ? {q: filtVal} : {};
        $.get(this.soundcloudUrl, query, function(resp) {
            var songs = resp.songs;
            player.playSongs(songs);
        });
    }
};

$(document).ready(function() {
    page.init();
});