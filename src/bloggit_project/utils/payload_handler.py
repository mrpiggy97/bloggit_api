
def payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user':{
            'username': user.username
        }
    }