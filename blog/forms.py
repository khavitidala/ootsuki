from django import forms
from .models import Post, Comment, Category

class CreatePost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'keyword', 'category', 'article', 'thumb_url', 'caption']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'comment']

