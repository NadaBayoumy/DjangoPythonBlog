from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Category (models.Model):
    categoryName = models.CharField(max_length = 180)
    #this line is commented because the admin is obligated to assign users for each category at creation of category and this is not true
    users = models.ManyToManyField(User, null = True ,blank = True)
    def __str__(self):
        return self.categoryName

class Post (models.Model):
    postTitle = models.CharField(max_length = 180)
    postPic = models.ImageField(verbose_name = "Post Image", upload_to = "static/img")
    postContent = models.TextField()
    userID = models.ForeignKey(User , related_name = 'users')
    postDate = models.DateTimeField(auto_now_add = True)
    postCategory = models.ForeignKey(Category)
    
    def __str__(self):
        return self.postTitle
       
       
class Reply (models.Model):
    replyContent = models.TextField()
    comment = models.ForeignKey('self', null = True, blank = True)
    userID = models.ForeignKey(User)
    replyDate = models.DateTimeField(auto_now_add = True)
    postID = models.ForeignKey(Post)
    
    replyContent.short_description = "reply"
    
    def __str__(self):
        return str(self.comment)


class ForbiddenWords(models.Model):
    forbiddenWord = models.CharField(max_length = 180)
    
    
    
    
    
    
    
    
    
    
