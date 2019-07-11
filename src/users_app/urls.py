#urls for users_app

from django.urls import path

from .views.CommunitiesFollowed import CommunitiesFollowed
from .views.ProfileData  import ProfileData

app_name = 'users_app'

urlpatterns = [
    #subscribe url
    path('subscribe/<slug:community_slug>/', CommunitiesFollowed.as_view(),
                                                name='subscribe'),
    #unsubscribe url
    path('unsubscribe/<slug:community_slug>', CommunitiesFollowed.as_view(),
                                                name='unsubscribe'),
    path('profile/<str:sub_uuid>/', ProfileData.as_view(), name='profile'),
]