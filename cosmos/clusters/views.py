from django.shortcuts import render,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
    ListView,
    RedirectView
)
#from django.views.generic import DetailView,ListView,RedirectView
#from django.views.generic import ListView  
#from django.views.generic import RedirectView 
from clusters.models import Cluster,ClusterMember
from django.contrib import messages

class CreateCluster(LoginRequiredMixin,CreateView):
    fields = ('name', 'description')
    model = Cluster

class SingleCluster(DetailView):
    model = Cluster

class ListClusters(ListView):
    model = Cluster
    #queryset = model.objects.order_by('name')

class JoinCluster(LoginRequiredMixin,RedirectView):
    
    def get_redirect_url(self, *args, **kwargs):
        return reverse("clusters:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):
        cluster = get_object_or_404(Cluster,slug=self.kwargs.get("slug"))

        try:
            ClusterMember.objects.create(user=self.request.user,cluster=cluster)

        except IntegrityError:
            messages.warning(self.request,("Warning, already a member of {}".format(cluster.name)))

        else:
            messages.success(self.request,"You are now a member of the {} cluster.".format(cluster.name))

        return super().get(request, *args, **kwargs)


class LeaveCluster(LoginRequiredMixin,RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("clusters:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):

        try:

            membership = ClusterMember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get("slug")
            ).get()

        except ClusterMember.DoesNotExist:
            messages.warning(
                self.request,
                "You can't leave this group because you aren't in it."
            )
        else:
            membership.delete()
            messages.success(
                self.request,
                "You have successfully left this group."
            )
        return super().get(request, *args, **kwargs)