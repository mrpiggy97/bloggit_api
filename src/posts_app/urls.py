#posts_app.urls

from django.urls import path
from .views.PostView import PostView
from .views.PostsByCommunity import PostsByCommunity
from .views.CommentView import CommentView

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
    #posts-by-community url
    path('posts-by-community/<slug:community_slug>/', PostsByCommunity.as_view(),
                                                        name='posts_by_community'),
    #get-comment url
    path('get-comment/<uuid:comment_uuid>/', CommentView.as_view(), name='get_comment'),
    #edit-comment url
    path('edit-comment/<uuid:comment_uuid>/',  CommentView.as_view(), name='edit_comment'),
    #make-comment url
    path('make-comment/', CommentView.as_view(), name='make_comment'),
    #delete-comment url
    path('delete-comment/<uuid:comment_uuid>/', CommentView.as_view(), name='delete_comment'),
]