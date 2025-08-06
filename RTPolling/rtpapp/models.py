from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Poll(models.Model):
    title = models.CharField(max_length=225)
    description = models.CharField(max_length=1225, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Option(models.Model):
    title = models.CharField(max_length=125)
    description = models.CharField(max_length=225, blank=True, null=True)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'poll')

    def __str__(self):
        return f"{self.user.username} voted {self.option.title} on {self.poll.title}."
