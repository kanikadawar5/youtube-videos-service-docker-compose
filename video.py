class Video:

    def __init__(self, title, description, thumbnails, publish_time, videoId, tags):
        self.title = title
        self.description = description
        self.thumbnails = thumbnails
        self.publish_time = publish_time
        self.videoId = videoId
        self.tags = tags

    def __str__(self):
        return "Video[title= %s description= %s publish_time = %s videoId = %s tags = %s]" % (self.title, self.description, self.publish_time, self.videoId, self.tags)
