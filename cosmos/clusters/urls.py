from django.urls import path, re_path
from . import views

app_name = 'clusters'

urlpatterns = [
    path('',views.ListView.as_view(),name="all"),
    path('new/',views.CreateCluster.as_view(),name="create"),
    re_path(r"^posts/in/(?P<slug>[-\w]+)/$",views.SingleCluster.as_view(),name="single")
]