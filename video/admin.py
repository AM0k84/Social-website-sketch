from django.contrib import admin
from embed_video.admin import AdminVideoMixin

from video.models import Video, VideoCategory, VideoComment


class VideoAdmin(AdminVideoMixin, admin.ModelAdmin):
    list_display = ('id', 'video_title', 'author', 'created_on', 'is_promoted', 'slug')  # todo: DODAĆ LISTE KATEGORII JAKO STRING
    prepopulated_fields = {'slug': ('video_title', )}



class VideoCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name', 'created_on', 'slug')
    prepopulated_fields = {'slug': ('category_name', )}

class VideoCommentAdmin(admin.ModelAdmin):
    list_display = ('video', 'author', 'title', 'created_on')


admin.site.register(VideoCategory, VideoCategoryAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(VideoComment, VideoCommentAdmin)
