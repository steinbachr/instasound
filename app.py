import get_tracks as gt

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

controller = gt.Controller()

@app.route('/')
def index():
    return render_template('index.html', )

@app.route('/play-soundcloud')
def play_soundcloud_songs():
    filt_val = request.args.get('q', None)
    songs = controller.get_soundcloud_songs(filter_val=filt_val)
    return jsonify(songs=songs)



if __name__ == '__main__':
    app.run(debug=True)