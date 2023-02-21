from django.db import models
from Accounts.models import Account
from ckeditor_uploader.fields import RichTextUploadingField 
from autoslug import AutoSlugField



class Post(models.Model):
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from='title', unique=True, default='slug')
    title = models.TextField(max_length=200, unique=True)
    image = models.ImageField(upload_to='blog_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = RichTextUploadingField() 


    def __str__(self):  
        return self.title  


class Post_Comment(models.Model):
    postId = models.ForeignKey(Post, on_delete=models.DO_NOTHING)
    subject = models.CharField(max_length = 10, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(auto_now=True)
    content = models.TextField()
    
    def __str__(self):
        return self.subject





