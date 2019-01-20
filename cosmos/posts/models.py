from django.db import models
from django.urls import reverse
from django.conf import settings
import misaka

from clusters.models import Cluster

from django.contrib.auth import get_user_model

User = get_user_model()

class Post(models.Model):
    user = models.ForeignKey(User,verbose_name="posts")
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)
    cluster = models.ForeignKey(Cluster,verbose_name="posts",null=True,blank=True)

    def __str__(self):
        return self.message

    def save(save,*args,**kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('posts:single', kwargs={'username':self.user.username,'pk':self.pk})

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user','message']