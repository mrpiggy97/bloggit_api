#like and and report post and comments

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from posts_app.models import Post, Comment

from users_app.models import Sub

from bloggit_project.utils.permissions import AuthenticatedAndOwnerOnly


@api_view(["PUT"])
@permission_classes([AuthenticatedAndOwnerOnly])
def like_post(request, post_uuid):
    '''increase post likes and add'''
    '''post uuid to sub.liked_posts'''
    
    post = Post.objects.get(uuid=post_uuid)
    session_sub = Sub.objects.get(user=request.user)
    liked_posts = session_sub.liked_posts_as_list
    
    if str(post.uuid) in liked_posts:
        status_code = status.HTTP_501_NOT_IMPLEMENTED
        return Response(data=None, status=status_code)
    
    elif str(post.uuid) not in liked_posts:
        liked_posts.append(str(post.uuid))
        session_sub.liked_posts_as_list = liked_posts
        post.likes = post.likes + 1
        post.save()
        
        status_code = status.HTTP_200_OK
        
        return Response(data=None, status=status_code)


@api_view(["PUT"])
@permission_classes([AuthenticatedAndOwnerOnly])
def like_comment(request, comment_uuid):
    '''increase comment likes and add'''
    '''comment uuid to sub.liked_comments'''
    
    comment = Comment.objects.get(uuid=comment_uuid)
    session_sub = Sub.objects.get(user=request.user)
    liked_comments = session_sub.liked_comments_as_list
    
    if str(comment.uuid) in liked_comments:
        status_code = status.HTTP_501_NOT_IMPLEMENTED
        return Response(data=None, status=status_code)
    
    else:
        liked_comments.append(str(comment.uuid))
        session_sub.liked_comments_as_list = liked_comments
        comment.likes = comment.likes + 1
        comment.save()
        
        status_code = status.HTTP_200_OK
        
        return Response(data=None, status=status_code)


@api_view(["PUT"])
@permission_classes([AuthenticatedAndOwnerOnly])
def report_post(request, post_uuid):
    '''increase post.likes and add its'''
    '''uuid to sub.reported_posts'''
    
    post = Post.objects.get(uuid=post_uuid)
    session_sub = Sub.objects.get(user=request.user)
    reported_posts = session_sub.reported_posts_as_list
    
    if str(post.uuid) in reported_posts:
        status_code = status.HTTP_501_NOT_IMPLEMENTED
        return Response(data=None, status=status_code)
    else:
        reported_posts.append(str(post.uuid))
        session_sub.reported_posts_as_list = reported_posts
        post.reports = post.reports + 1
        post.save()
        
        status_code = status.HTTP_200_OK
        return Response(data=None, status=status_code)


@api_view(["PUT"])
@permission_classes([AuthenticatedAndOwnerOnly])
def report_comment(request, comment_uuid):
    '''increase comment.reports number and add'''
    '''its uuid to sub.reported_comments'''
    
    comment = Comment.objects.get(uuid=comment_uuid)
    session_sub = Sub.objects.get(user=request.user)
    reported_comments = session_sub.reported_comments_as_list
    
    if str(comment.uuid) in reported_comments:
        status_code = status.HTTP_501_NOT_IMPLEMENTED
        return Response(data=None, status=status_code)
    else:
        reported_comments.append(str(comment.uuid))
        session_sub.reported_comments_as_list = reported_comments
        comment.reports = comment.reports + 1
        comment.save()
        
        status_code = status.HTTP_200_OK
        
        return Response(data=None, status=status_code)