from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from django.http import Http404
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
    ListView,
    RedirectView
)
from django.contrib import messages
from braces.views import SelectRelatedMixin
#from . import forms

from . import models


from django.contrib.auth import get_user_model

User = get_user_model()

class PostList(SelectRelatedMixin,ListView):
    model = models.Post
    select_related = ('user', 'cluster')

class UserPosts(ListView):
    model = models.Post
    template_name = 'posts/user_post_list.html'

    def get_queryset(self):
        
        try:
            self.post_user = User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))

        except User.DoesNotExist:
            raise Http404
        
        else:
            return self.post_user.posts.all()
            
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        return context

class PostDetail(SelectRelatedMixin,DetailView):
    model = models.Post
    select_related = ('user','cluster')

    def get_queryset(self,**kwargs):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))

class CreatePost(LoginRequiredMixin,SelectRelatedMixin,CreateView):
    
    model = models.Post
    fields = ('message','cluster',)
    #form_class = forms.PostForm

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

class DeletePost(LoginRequiredMixin,SelectRelatedMixin,DeleteView):

    model = models.Post
    select_related = ('user', 'cluster')   

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id = self.request.user.id)

    def delete(self,*args,**kwargs):
        messages.success(self.request,'Post Deleted')
        return super().delete(*args,**kwargs)
