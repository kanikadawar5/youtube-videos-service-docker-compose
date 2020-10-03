from pymongo import MongoClient, DESCENDING, TEXT
import ssl
import datetime
from googleapiclient.discovery import build
# from flask_paginate import Pagination, get_page_args
# from flask.ext.paginate import Pagination
# page, per_page, offset = get_page_items()
from bson.json_util import dumps


class DbManager:

    def createIndexes(self):
        self.collection.create_index([('publishedAt', DESCENDING)], background=True)
        self.collection.create_index('videoId', background=True, unique=True)
        self.collection.create_index([('description', TEXT), ('title', TEXT)], default_language='english')

    def __init__(self):
        # mongo_client = "mongodb://localhost:27017/"
        # db_name = "db"
        # collection_name = "users"
        self.client = MongoClient("mongodb://my_mongodb:27017", ssl_cert_reqs=ssl.CERT_NONE)
        self.db = self.client.youtube
        self.collection = self.db.videos
        self.DEVELOPER_KEY = 'AIzaSyAcZ2kQyUI1cf_xG7WKAiJYdJD0Se0FC8c'
        self.YOUTUBE_API_SERVICE_NAME = 'youtube'
        self.YOUTUBE_API_VERSION = 'v3'
        self.nextPageToken = None
        self.createIndexes()

    def __str__(self):
        return "DB[db= %s collection %s ]" % (self.db, self.collection)

    def fetch(self, page_num, limit):
        skips = limit * (page_num - 1)
        return dumps(self.collection.find().sort([("publishedAt", -1)]).skip(skips).limit(limit))

    def insert(self, objects):
        try:
            self.collection.insert_many(objects)
        except pymongo.errors.BulkWriteError as e:
            print("bulk insert error", str(e.message))

    def search(self, query):
        cursor = self.collection.find({"$text": {"$search": query}})

        videos = []
        for entry in cursor:
            data = {}
            data['title'] = entry.get('title', '')
            data['description'] = entry.get('description', '')
            data['thumbnails'] = entry.get('thumbnails', {})
            data['publishedAt'] = entry.get('publishedAt', None)
            data['videoId'] = entry.get('videoId', None)
            videos.append(data)

        return videos

    def fetch_videos_from_youtube(self, search_query):
        youtube = build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION,
                        developerKey=self.DEVELOPER_KEY)

        search_response = youtube.search().list(
            q=search_query,
            part='id,snippet',
            pageToken=self.nextPageToken,
            publishedAfter=datetime.datetime.now().isoformat() + "Z",
            maxResults=50
        ).execute()

        videos = []

        for search_result in search_response.get('items', []):
            if search_result['id']['kind'] == 'youtube#video':
                data = {}
                data['thumbnails'] = search_result['snippet']['thumbnails']
                data['description'] = search_result['snippet']['description']
                data['title'] = search_result['snippet']['title']
                data['publishedAt'] = search_result['snippet']['publishedAt']
                data['videoId'] = search_result['id']['videoId']

                videos.append(data)

        return videos

    def fetch_and_save_videos_from_youtube(self, search_query):
        videos = self.fetch_videos_from_youtube(search_query)
        self.insert(videos)
