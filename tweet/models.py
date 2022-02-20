# tweet/models.py
from django.db import models
from user.models import UserModel
from taggit.managers import TaggableManager
#user앱에 있는 model을 가져와서 사용할건데 model중에서 이름이 UserModel인 걸 가져와서 사용하겠단 의미


# Create your models here.
class TweetModel(models.Model):
    class Meta:
        db_table = "tweet"
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    content = models.CharField(max_length=256)
    tags = TaggableManager(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class TweetComment(models.Model):
    class Meta:
        db_table = "comment"
    tweet = models.ForeignKey(TweetModel, on_delete=models.CASCADE)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    comment = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)