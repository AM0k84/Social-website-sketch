from django import forms

from .models import Video, VideoComment

from tinymce.widgets import TinyMCE


class AddVideoForm(forms.ModelForm):
    video_title = forms.CharField(
        label="Tytuł",
        max_length=120,
        help_text="Tytuł newsa",
        widget=forms.TextInput(attrs={"class": "form-control form-control-lg pr-5 shadow p-1 mb-1 bg-white rounded"}),
        required=True,
    )

    youtube_video = forms.URLField(
        label="Video",
        max_length=500,
        help_text="Link do video w serwisie YouTube",
        widget=forms.URLInput(attrs={"class": "form-control form-control-lg pr-5 shadow p-2 mb-1 bg-white rounded"}),
        required=True,
    )

    snippet = forms.CharField(
        label="Snippet",
        max_length=300,
        help_text="Krótki opis",
        widget=forms.Textarea(attrs={"class": "form-control form-control-lg pr-5 shadow p-1 mb-1 bg-white rounded"}),
        required=True,

    )

    body = forms.CharField(
        label="Opis video",
        max_length=500,
        help_text="Długi opis video",
        widget=TinyMCE(attrs={"class": "form-control form-control-lg pr-5 shadow p-1 mb-1 bg-white rounded"}),
        required=True,
    )




    class Meta:
        model = Video
        fields = ('video_title', 'youtube_video', 'category', 'snippet', 'body')


class EditVideoForm(forms.ModelForm):

    video_title = forms.CharField(
        label="Tytuł",
        max_length=120,
        help_text="Tytuł newsa",
        widget=forms.TextInput(attrs={"class": "form-control form-control-lg pr-5 shadow p-1 mb-1 bg-white rounded"}),
        required=True,
    )

    youtube_video = forms.URLField(
        label="Video",
        max_length=500,
        help_text="Link do video w serwisie YouTube",
        widget=forms.URLInput(attrs={"class": "form-control form-control-lg pr-5 shadow p-2 mb-1 bg-white rounded"}),
        required=True,
    )

    snippet = forms.CharField(
        label="Snippet",
        max_length=300,
        help_text="Krótki opis",
        widget=forms.Textarea(attrs={"class": "form-control form-control-lg pr-5 shadow p-1 mb-1 bg-white rounded"}),
        required=True,

    )

    body = forms.CharField(
        label="Opis video",
        max_length=500,
        help_text="Długi opis video",
        widget=TinyMCE(attrs={"class": "form-control form-control-lg pr-5 shadow p-1 mb-1 bg-white rounded"}),
        required=True,
    )

    class Meta:
        model = Video
        fields = ('video_title', 'youtube_video', 'category', 'snippet', 'body')


class VideoCommentForm(forms.ModelForm):

    title = forms.CharField(
        label="Tytuł",
        max_length=120,
        widget=forms.TextInput(attrs={"class": "form-control form-control-lg col-6 pr-5 shadow p-1 mb-1 bg-white rounded"}),
        required=True,
    )

    body = forms.CharField(
        label="Treść komentarza",
        max_length=300,
        widget=forms.Textarea(attrs={"class": "form-control form-control-lg col-6 pr-5 shadow p-1 mb-1 bg-white rounded"}),
        required=True,

    )
    class Meta:
        model = VideoComment
        fields = ('title', 'body', )
