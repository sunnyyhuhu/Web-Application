from django.db import models
from django.contrib.auth.models import User

class Entry(models.Model):
    first_name = models.CharField(max_length=20)
    last_name  = models.CharField(max_length=20)
    username   = models.CharField(max_length=20)
    password   = models.CharField(max_length = 200)
    confirm_password = models.CharField(max_length = 200)
    email      = models.CharField(max_length=32)
    def __str__(self):
        return 'Entry(id=' + str(self.id) + ')'

class Post(models.Model):
    user    = models.ForeignKey(User, on_delete=models.PROTECT, related_name="post_creators")
    creation_time  = models.DateTimeField()
    text  = models.CharField(max_length = 200)

class Profile(models.Model):
    user      = models.OneToOneField(User, on_delete=models.PROTECT)
    bio_text  = models.CharField(max_length = 200)
    picture = models.FileField(blank=True)
    content_type = models.CharField(max_length=50)
    following = models.ManyToManyField(User, related_name = 'followers')


