from django.db import models

# Create your models here.

class Tweets(models.Model):
    Lang = models.CharField(max_length=10)
    Day_time_date = models.CharField(max_length=30)
    Text = models.CharField(max_length=400)
    Fav_count = models.CharField(max_length=10)
    Ret_count = models.CharField(max_length=10)
    Hashtag = models.CharField(max_length=200)
