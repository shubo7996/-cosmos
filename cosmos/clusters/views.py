from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from clusters.models import Cluster
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView
)
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView   

class CreateCluster(LoginRequiredMixin,CreateView):
    fields = ('name', 'description')
    model = Cluster

class SingleCluster(DetailView):
    model = Cluster

class ListCluster(ListView):
    model = Cluster
