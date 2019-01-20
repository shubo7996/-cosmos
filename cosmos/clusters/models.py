from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
import misaka
from django.urls import reverse

from django import template
register = template.Library()

User = get_user_model()

class Cluster(models.Model):
    name = models.CharField(max_length=255,unique=True)
    slug = models.SlugField(allow_unicode= True, unique= True)
    description = models.CharField(blank= True, default= '' )
    description_html = models.TextField(editable=False,default='',blank=True)
    members = models.ManyToManyField(User,through= 'ClusterMember')

    def __str__(self):
        self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.description_html = misaka(self.description)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('clusters:single',kwargs={'slug':self.slug})

    class Meta:
        ordering = ('name')

class ClusterMember(models.Model):
    cluster = models.ForeignKey(
        Cluster,
        verbose_name = 'subscription'
    )

    user = models.ForeignKey(
        User,
        verbose_name = 'user_clusters'
    )

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('cluster','user')



