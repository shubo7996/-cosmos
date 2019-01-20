from django.contrib import admin
from . import models

# Register your models here.
class ClusterMemberInLine(admin.TabularInLine):
    model = models.ClusterMember

admin.site.register(models.Cluster)
