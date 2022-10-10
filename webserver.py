import asyncio
import logging

import requests
from flask import Flask, Response, render_template, request, jsonify
from flask_cors import CORS

from blackbird import find_username

app = Flask(__name__, static_folder='templates/static')
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
CORS(app, resources={r"/*": {"origins": "*"}})
loop = asyncio.get_event_loop()
logging.getLogger('werkzeug').disabled = True


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/search/username', methods=["POST"])
def search_username():
    content = request.get_json()
    username = content['username']
    interface_type = 'web'
    results = loop.run_until_complete(find_username(username, interface_type))
    return jsonify(results)


@app.route('/image', methods=["GET"])
def get_image():
    url = request.args.get('url')
    # noinspection PyBroadException
    try:
        image_binary = requests.get(url).content
        return Response(image_binary, mimetype='image/gif')
    except:
        return Response(status=500)


app.run(host='0.0.0.0', port=9797)
