from django import forms

from .models import ArticleComment, Article


class AddArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'image', 'category', 'snippet', 'body')






class EditArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'image', 'category', 'snippet', 'body')


class CommentForm(forms.ModelForm):
    class Meta:
        model = ArticleComment
        fields = ('title', 'body',)
