#posts_app.urls

from django.urls import path
from .views.PostView import PostView
from .views.PostsByCommunity import PostsByCommunity
from .views.SearchView import SearchView
from .views.GenericListAPIViews import HomeView, PopularInCommunity
from .views.CommentView import CommentView

app_name = 'posts_app'
urlpatterns = [
    #home url
    path('', HomeView.as_view(), name='home'),
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
    #most popular posts in community url
    path('most-popular/<slug:community_slug>/', PopularInCommunity.as_view(),
         name='most_popular'),
    #search-view
    path('search/<str:query>/', SearchView.as_view(), name='search'),
    #get-comment url
    path('get-comment/<str:comment_uuid>/', CommentView.as_view(), name='get-comment'),
    #make-original-comment url
    path('make-original-comment/', CommentView.as_view(),
         {'is_original': True}, name='make_original_comment'),
    #make-child-comment url
    path('make-child-comment/', CommentView.as_view(),
         {'is_original': False}, name='make_child_comment'),
    #update-original-comment url
    path('update-original-comment/', CommentView.as_view(),
         {'is_original': True}, name='update_original_comment'),
    #update-child-comment url
    path('update-child-comment/', CommentView.as_view(),
         {'is_original': False}, name='update_child_comment'),
    #delete-comment url
    path('delete-comment/<str:comment_uuid>/', CommentView.as_view(),
         name='delete_comment'),
]