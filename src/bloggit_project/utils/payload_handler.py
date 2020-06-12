from users_app.models import Sub


def payload_handler(token, user=None, request=None):
    
    sub = Sub.objects.get(user=user)
    return {
        'token': token,
        'username': user.username,
        'profile_pic': sub.get_profile_pic_url,
        'communities': sub.get_communities_as_list,
        'authenticated' : True
    }