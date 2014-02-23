var page = {
    jPlayer: "#jquery_jplayer_1",
    filterCont: '.filters',
    msgCont: '.msg_container',

    soundcloudUrl: '/play-soundcloud',
    eightTracksUrl: '/play-8tracks',
    downloadUrl: '/download',

    mediaSource: 'soundcloud',
    mediaNameMap: {
        soundcloud: 'Soundcloud',
        '8tracks': '8tracks'
    },

    /*
    get the next song for the current mix from 8tracks (we have to do it this way because we cant just load up a bunch
    of songs like we do for soundcloud)
     */
    _getNext8tracksSong: function() {
        $.get(this.eightTracksUrl, {}, function(resp) {
            player.addSong(resp.song, true);
        });
    },

    /*
    compile the appropriate filters for the chosen mediaSource
     */
    _compileMediaFilters: function() {
        var tpl = _.template($('#filter_tpl').html()),
            compiled = tpl({
                mediaName: this.mediaNameMap[this.mediaSource],
                mediaSource: this.mediaSource
            });

        $('.filters').html(compiled);

        this.mediaSource == '8tracks' && $('select').fancySelect();
    },

    /*
    compile the error message if we've hit an error
    @param error - the error object
     */
    _compileErrorMsg: function(error) {
        var tpl = _.template($('#error_tpl').html()),
            compiled = tpl(error);

        $(this.msgCont).html(compiled);
    },

    /*
    compile the warning message when apropriate
    @param warning - the warning object
     */
    _compileWarningMsg: function(warning) {
        var tpl = _.template($('#warning_tpl').html()),
            compiled = tpl(warning);

        $(this.msgCont).html(compiled);
    },

    /*
    clear error message
     */
    _clearErrorMsg: function() {
        $(this.msgCont).html('');
    },

    init: function() {
        player.init(this.jPlayer, {}, false);

        this._compileMediaFilters();
        this.playSoundcloud();
        this.clickBindings();

        var _this = this;
        /* if the current media source is 8tracks, then when a song is done, we have to load the next song from the server */
        $(this.jPlayer).bind($.jPlayer.event.ended, function() {
            _this.mediaSource == '8tracks' && _this._getNext8tracksSong();
        })
    },

    clickBindings: function() {
        var _this = this;

        /* click bindings */
        $('.nav_item').click(function() {
            $('.nav_item').removeClass('selected');
            $(this).addClass('selected');
            _this.mediaSource = $(this).data('mediaSource');

            _this._compileMediaFilters();
            switch (_this.mediaSource) {
                case 'soundcloud':
                    _this.playSoundcloud();
                    break;
                case '8tracks':
                    _this.play8Tracks();
                    break;
                default:
                    break;
            }
        });

        $(this.filterCont).on('click', '.download', function() {
            var songUrl = $('.jp-playlist-current').find('a[data-download-url]').data('downloadUrl');
            _this._clearErrorMsg();

            if (songUrl) {
                _this.mediaSource == '8tracks' && _this._compileWarningMsg({warning: "downloaded files from 8tracks might not match correctly"});
                window.location = _this.downloadUrl + "?song=" + songUrl;
            } else {
                _this._compileErrorMsg({error: 'Sorry, this track isn\'t downloadable'});
            }
        });

        $(this.filterCont).on('click', '.apply_filters', function() {
            var filterVal = $(this).closest('.filters').find('input').val();
            _this._clearErrorMsg();

            switch (_this.mediaSource) {
                case 'soundcloud':
                    _this.playSoundcloud(filterVal);
                    break;
                case '8tracks':
                    var filterType = $(this).closest('.filters').find('select').val();
                    _this.play8Tracks(filterType, filterVal);
                    break;
                default:
                    break;
            }
        });
    },

    /*
    play songs from soundcloud
    @param filtVal - if provided, this is the filter
     */
    playSoundcloud: function(filtVal) {
        var query = filtVal ? {q: filtVal} : {};
        $.get(this.soundcloudUrl, query, function(resp) {
            player.playSongs(resp.songs);
        });
    },

    /*
    play songs from 8tracks
    @param filtType - the type of the filter being applied (keyword, artist, tag)
    @param filtVal - if provided this is the filter to apply when fetching a mix
     */
    play8Tracks: function(filtType, filtVal) {
        var query = filtVal ? {qType: filtType, q: filtVal} : {},
            _this = this;
        $.get(this.eightTracksUrl, $.extend({}, query, {first: true}), function(resp) {
            resp.song ? player.playSongs([resp.song]) : _this._compileErrorMsg(resp);
        });
    }
};

$(document).ready(function() {
    page.init();
});