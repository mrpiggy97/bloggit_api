#urls for users_app

from django.urls import path

from .views.CommunitiesFollowed import CommunitiesFollowed
from .views.ProfileData  import ProfileData
from .views.LikesReports import like_post, like_comment, report_post, report_comment

app_name = 'users_app'

urlpatterns = [
    #subscribe url
    path('subscribe/<slug:community_slug>/', CommunitiesFollowed.as_view(),
                                                name='subscribe'),
    #unsubscribe url
    path('unsubscribe/<slug:community_slug>', CommunitiesFollowed.as_view(),
                                                name='unsubscribe'),
    path('profile/<uuid:sub_uuid>/', ProfileData.as_view(), name='profile'),
    #like-post url
    path('like-post/<uuid:post_uuid>/', like_post, name='like_post'),
    #like-comment url
    path('like-comment/<uuid:comment_uuid>/', like_comment, name='like_comment'),
    #report-post url
    path('report-post/<uuid:post_uuid>/', report_post, name='report_post'),
    #report-comment url
    path('report-comment/<uuid:comment_uuid>/', report_comment, name='report_comment'),
]