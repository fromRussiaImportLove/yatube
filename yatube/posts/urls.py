from django.urls import path

from posts import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new_post, name='new_post'),
    path('group/<slug:slug>/', views.group_posts, name='group_posts'),
    path('follow/', views.follow_index, name='follow_index'),
    path('<str:username>/', views.profile, name='profile'),
    path('<str:username>/<int:post_id>/', views.post_detail, name='post_view'),
    path('<str:username>/<int:post_id>/edit/',
         views.post_edit, name='post_edit'),
    path('<str:username>/<int:post_id>/comment/',
         views.add_comment, name='add_comment'),
    path('<str:username>/follow/',
         views.profile_follow, name='profile_follow'),
    path('<str:username>/unfollow/',
         views.profile_unfollow, name='profile_unfollow'),
]
