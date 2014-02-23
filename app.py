import get_tracks as gt
from eight_py import Api
from flask import Flask, render_template, request, jsonify, Response, make_response
import pdb
import urllib

app = Flask(__name__)

API_KEY = '7fe2e057bb81abf2248a06ecab027b8dc09e01d3'
eight_py = Api(api_key=API_KEY)
controller = gt.Controller(eight_py)

@app.route('/')
def index():
    return render_template('index.html', )

@app.route('/play-soundcloud')
def play_soundcloud_songs():
    filt_val = request.args.get('q', None)
    songs = controller.get_soundcloud_songs(filter_val=filt_val)
    return jsonify(songs=songs)

@app.route('/play-8tracks')
def play_8tracks_songs():
    filt_type = request.args.get('qType', None)
    filt_val = request.args.get('q', None)
    first_track = request.args.get('first', None)

    song = controller.get_8tracks_song(filter_type=filt_type, filter_val=filt_val, starting_playback=first_track)
    return jsonify(song=song) if song else jsonify(error='No songs found with given filters')

@app.route('/download')
def download_song():
    song_url = request.args.get('song')
    download_resp = controller.download(song_url)
    resp_headers = download_resp.headers

    return Response(download_resp.content, content_type=resp_headers['content-type'], headers={
        'Content-Disposition': resp_headers['content-disposition']
    })


if __name__ == '__main__':
    app.run(debug=True)