$(document).ready(function() {
    player.init("#jquery_jplayer_1", {}, false);

    $.get('/play-soundcloud', {}, function(resp) {
        var songs = resp.songs;
        player.playSongs(songs);
    });
})