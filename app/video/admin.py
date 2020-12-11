from django.contrib import admin

# Registering Video Model
from video.models import Video


class VideoAdmin(admin.ModelAdmin):
    sortable_by = ('published_at',)
    list_display = ('yt_id', 'title', 'published_at')


admin.site.register(Video, VideoAdmin)
