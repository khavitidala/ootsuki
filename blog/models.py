from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField

class Category(models.Model):
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    templ_id = models.CharField(max_length=200, null=False)
    title = models.CharField(max_length=200, null=False)
    keyword = models.CharField(max_length=500, null=True)
    category = models.ManyToManyField(Category)
    article = RichTextField(blank=True, null=True)
    thumb_url = models.URLField(null=True) 
    caption = models.CharField(max_length=200, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    comment = models.TextField(max_length=500)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    img_url = models.CharField(max_length=100)
    email = models.EmailField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment
    
    def __str__(self):
        return self.name