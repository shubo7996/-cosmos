from django.test import TestCase
from .models import Post
from django.utils import timezone
from django.urls import reverse
from clusters.models import Cluster
from django.contrib.auth.models import User


# models test
class PostTest(TestCase):

    def setup(self):
        user = User.objects.create('subhamholla', 'subha@xyz.com','subhamoy')
        clusters = Cluster.objects.create(name="Supernova",description="test supernova",members = user)
        Post.objects.create(user=user,message="hello",cluster=clusters, created_at=timezone.now())

    def test_post_creation(self):
        obj = Post.objects.get(id=1)
        self.assertEqual(obj.__self__(), obj.message)