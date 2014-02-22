$(document).ready(function() {
    player.init("#jquery_jplayer_1", {}, false);

    $.get('/play-soundcloud', {}, function(resp) {
        var songs = resp.songs;
        var songObjs = songs.map(function(s) {
            return {
                title: s.title,
                artist: s.artist,
                mp3: s.mp3,
                poster: ''
            }
        });
        player.playSongs(songObjs);
    });

    $('.nav_item').click(function() {
        $('.nav_item').removeClass('selected');
        $(this).addClass('selected');
    })
});