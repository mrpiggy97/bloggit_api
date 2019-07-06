#posts_app.urls

from django.urls import path
from .views.PostView import PostView

app_name = 'posts_app'
urlpatterns = [
    #get-post url
    path('get-post/<str:post_uuid>/', PostView.as_view(), name='get_post'),
    #edit-post url
    path('edit-post/<str:post_uuid>/', PostView.as_view(), name='edit_post'),
    #make-post url
    path('make-post/', PostView.as_view(), name='make_post'),
    #delete-post url
    path('delete-post/<str:post_uuid>/', PostView.as_view(), name='delete_post'),
]