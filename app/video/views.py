from rest_framework import generics

from video.models import Video
from video.serializers import VideoSerializer


class VideoList(generics.ListAPIView):
    """Endpoint that will list all videos in a paginated response"""
    serializer_class = VideoSerializer
    queryset = Video.objects.all()
