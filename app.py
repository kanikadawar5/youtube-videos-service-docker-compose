from flask import Flask, render_template, request

from werkzeug.wrappers import Response
import time
import json
from concurrent.futures import ThreadPoolExecutor, wait
from db import DbManager

app = Flask(__name__)

SEARCH_QUERY_CRICKET = 'news'


@app.route('/')
def dashboard_home():
    return render_template('index.html')


@app.route('/get_videos', methods=['GET'])
def get_videos():
    db_manager = DbManager()
    page_num = request.args.get('page_num', 1, type=int)
    limit = request.args.get('limits', 5, type=int)
    data = db_manager.fetch(page_num, limit)
    return Response(status=200, response=data)


@app.route('/search', methods=['GET'])
def search_videos():
    query = request.args.get('query', '')

    if not query:
        return Response(status=400, response='Empty search query provided')

    db_manager = DbManager()
    list_videos = db_manager.search(query)
    data = {}
    data["no_of_videos"] = len(list_videos)
    data["videos"] = list_videos
    return Response(status=200, response=json.dumps(data))


def load_data_in_bg():
    db_manager = DbManager()
    while True:
        db_manager.fetch_and_save_videos_from_youtube(SEARCH_QUERY_CRICKET)
        time.sleep(5)


if __name__ == '__main__':
    # Creating a new thread and loading the videos in the database by hitting the youtube APIs
    pool = ThreadPoolExecutor(1)
    pool.submit(load_data_in_bg)

    app.run(host='0.0.0.0')
