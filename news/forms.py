from django import forms

from tinymce.widgets import TinyMCE

from .models import ArticleComment, Article


class AddArticleForm(forms.ModelForm):
    title = forms.CharField(
        label="Tytuł",
        max_length=120,
        help_text="Tytuł newsa",
        widget=forms.TextInput(attrs={"class": "form-control form-control-lg pr-5 shadow p-1 mb-1 bg-white rounded"}),
        required=True,
    )

    image = forms.ImageField(
        label="Zdjęcie",
        help_text="Akceptowane pliki to: jpg....",
        widget=forms.ClearableFileInput(
            attrs={"class": "form-control form-control pr-3 shadow p-1 mb-1 bg-white rounded"}), required=True,
    )

    snippet = forms.CharField(
        label="Snippet",
        max_length=300,
        help_text="Krótki opis",
        widget=forms.Textarea(attrs={"class": "form-control form-control-lg pr-5 shadow p-1 mb-1 bg-white rounded"}),
        required=True,

    )

    body = forms.CharField(
        label="Treść newsa",
        max_length=500,
        help_text="Długi opis",
        widget=TinyMCE(attrs={"class": "form-control form-control-lg pr-5 shadow p-1 mb-1 bg-white rounded"}),
        required=True,
    )

    class Meta:
        model = Article
        fields = ('title', 'image', 'category', 'snippet', 'body')
        widgets = {
            'category': forms.CheckboxSelectMultiple(attrs={"class": "column-checkbox"}),
        }
        labels = {
            'category': 'Kategorie',

        }
        help_texts = {'category': 'Możliwy wielokrotny wybór'}


class EditArticleForm(forms.ModelForm):
    title = forms.CharField(
        label="Tytuł",
        max_length=120,
        help_text="Tytuł newsa",
        widget=forms.TextInput(attrs={"class": "form-control form-control-lg pr-5 shadow p-1 mb-1 bg-white rounded"}),
        required=True,
    )

    image = forms.ImageField(
        label="Zdjęcie",
        help_text="Akceptowane pliki to: jpg....",
        widget=forms.ClearableFileInput(
            attrs={"class": "form-control form-control pr-3 shadow p-1 mb-1 bg-white rounded"}), required=True,
    )

    snippet = forms.CharField(
        label="Snippet",
        max_length=300,
        help_text="Krótki opis",
        widget=forms.Textarea(attrs={"class": "form-control form-control-lg pr-5 shadow p-1 mb-1 bg-white rounded"}),
        required=True,

    )

    body = forms.CharField(
        label="Treść newsa",
        max_length=500,
        help_text="Długi opis",
        widget=TinyMCE(attrs={}),
        required=True,
    )

    class Meta:
        model = Article
        fields = ('title', 'image', 'category', 'snippet', 'body')
        widgets = {
            'category': forms.CheckboxSelectMultiple(attrs={"class": "Col-2"}),
        }
        labels = {
            'category': 'Kategorie',

        }
        help_texts = {'category': 'Możliwy wielokrotny wybór'}


class CommentForm(forms.ModelForm):
    title = forms.CharField(
        label="Tytuł",
        max_length=120,
        widget=forms.TextInput(
            attrs={"class": "form-control form-control-lg col-6 pr-5 shadow p-1 mb-1 bg-white rounded"}),
        required=True,
    )

    body = forms.CharField(
        label="Treść komentarza",
        max_length=300,
        widget=forms.Textarea(
            attrs={"class": "form-control form-control-lg col-6 pr-5 shadow p-1 mb-1 bg-white rounded"}),
        required=True,

    )

    class Meta:
        model = ArticleComment
        fields = ('title', 'body',)
