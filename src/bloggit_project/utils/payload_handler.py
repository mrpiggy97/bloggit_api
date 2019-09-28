
def payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'username': user.username
    }