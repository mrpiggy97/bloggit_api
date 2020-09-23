from users_app.models import Sub


def payload_handler(token, user=None, request=None, session_sub=None):
    #user should never be None
    if user is None:
        raise ValueError("user is not supposed to be none")
    if session_sub is None:
        session_sub = Sub.objects.get(user=user)
    return {
        'token': token,
        'username': user.username,
        'profile_pic': session_sub.get_profile_pic_url,
        'communities': session_sub.get_communities_as_list,
        'authenticated' : True
    }