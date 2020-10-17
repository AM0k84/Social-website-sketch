from django import forms

from .models import Video, VideoComment


class AddVideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('video_title', 'youtube_video', 'category', 'snippet', 'body')


class EditVideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('video_title', 'youtube_video', 'category', 'snippet', 'body')


class VideoCommentForm(forms.ModelForm):
    class Meta:
        model = VideoComment
        fields = ('title', 'body', )
