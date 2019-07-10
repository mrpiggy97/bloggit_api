#urls for users_app

from django.urls import path

from .views.CommunitiesFollowed import CommunitiesFollowed

app_name = 'users_app'

urlpatterns = [
    #subscribe url
    path('subscribe/<slug:community_slug>/', CommunitiesFollowed.as_view(),
                                                name='subscribe'),
    #unsubscribe url
    path('unsubscribe/<slug:community_slug>', CommunitiesFollowed.as_view(),
                                                name='unsubscribe'),
]