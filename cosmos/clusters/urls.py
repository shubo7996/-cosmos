from django.urls import path, re_path
from . import views

app_name = 'clusters'

urlpatterns = [
    path('',views.ListClusters.as_view(),name="all"),
    path('new/',views.CreateCluster.as_view(),name="create"),
    re_path(r"posts/in/(?P<slug>[-\w]+)/$",views.SingleCluster.as_view(),name="single"),
    re_path(r"join/(?P<slug>[-\w]+)/$",views.JoinCluster.as_view(),name="join"),
    re_path(r"leave/(?P<slug>[-\w]+)/$",views.LeaveCluster.as_view(),name="leave"),
]