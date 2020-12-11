from django.db import models


class Video(models.Model):
    """
       This model holds video details fetched through the async service
    """
    yt_id = models.CharField(max_length=32, unique=True)
    title = models.TextField()
    description = models.TextField()
    thumbnail_url = models.URLField()
    published_at = models.DateTimeField()

    class Meta:
        """
        Indexing for quick retrieval of videos by youtube id and by publishing
        date
        """
        indexes = [
            models.Index(fields=['yt_id']),
            models.Index(fields=['published_at'])
        ]
