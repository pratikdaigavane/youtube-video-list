from rest_framework import serializers

from video.models import Video


class VideoSerializer(serializers.ModelSerializer):
    """Serializer for Video"""

    class Meta:
        model = Video
        fields = ['yt_id', 'published_at', 'title', 'description',
                  'thumbnail_url', ]
