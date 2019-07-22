from django.contrib.auth.models import User

from users_app.models import Sub

from posts_app.models import Post

user_test_data = {
    'username': 'newusertesting23',
    'password': 'ldkkasl2334',
    'email': 'newemail@email.com'
    }
    
def create_user():
    return User.objects.create_user(**user_test_data)

def create_sub(user):
    return Sub.objects.create(user=user)

def create_post(owner):
    return Post.objects.create(
        title='this is the title',
        text='this is a test',
        owner=owner
    )