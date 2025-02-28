from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework import status
from posts.models import Post,UserAccount, Comments
from api.v1.posts.serializer import PostSerializer, DeletePostSerializer, MyPostSerializer, CommentSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    current_user = UserAccount.objects.filter(user = request.user)
    image = request.data.get('image')
    caption = request.data.get('caption')
    if current_user.exists():
        if image and caption:
            post = Post.objects.create(
                image=image,
                caption=caption,
                user_name=request.user
            )
            response_data = {
                'status_code': 6000,
                'message': 'Post created successfully'
            }
            return Response(response_data)
        else:
            response_data = {
                'status_code': 6001,
                'message': 'Please provide image and caption'
            }
            return Response(response_data)
    else:
        response_data = {
            'status_code': 6002,
            'message': 'Creat a profile before posting'
        }
        return Response(response_data)


@api_view(['GET'])
@permission_classes([AllowAny])
def posts(request):
    context = {
        'request': request
    }
    instances = Post.objects.filter(is_deleted = False)
    serializer = PostSerializer(instances, many = True, context = context)

    response_data = {
        'status_code' : 6000,
        'data':serializer.data
    }

    return Response(response_data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def delete_post(request,id):
    if Post.objects.filter(pk = id).exists():
        instances = Post.objects.get(pk = id)
        serializer = DeletePostSerializer(instance = instances, data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            
            response_data = {
                'status_code' : 6000,
                'message': 'post deleted successfully',
            }
            return Response(response_data)
        else:

            response_data = {
                'status_code': 6001,
                'message' : 'Some error'
            }
            return Response(response_data)
    else:
        response_data = {
            'status_code': 6001,
            'message' : 'Some error'
        }
        return Response(response_data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_post(request,id):
    if Post.objects.filter(pk = id).exists():
        instances = Post.objects.get(pk = id)
        serializer = PostSerializer(instance = instances, data = request.data, partial = True)

        if serializer.is_valid():
            serializer.save()

            response_data = {
                'status_code':6000,
                'message':'Post edited successsfully'
            }
            return Response(response_data)
        else:
            response_data = {
                'status_code':6001,
                'message':'Not valid'
            }
            return Response(response_data)
    else:
        response_data = {
            'status_code':6001,
            'messageser_profile = UserProfile.objects.get() ':'Post not existed'
        }
        return Response(response_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_post(request):
    context = {
        "request":request
    }
    instances = Post.objects.filter(user_name = request.user, is_deleted = False)
    if instances:
        serializer = MyPostSerializer(instances, many = True, context = context)
        response_data = {
            "status_code" : 6000,
            "data":serializer.data
        }
        return  Response(response_data)
    else:
        response_data = {
            "status_code": 6001,
            "message": "No posts found"
        }
        return  Response(response_data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like(request,id):
    if Post.objects.filter(pk = id).exists():
        post = Post.objects.get(pk = id)
        current_user = UserAccount.objects.get(user = request.user)

        if current_user in post.like.all():
            post.like.remove(current_user)
            post.update_like_count()

            response_data = {
                'status_code' : 6000,
                'message' : 'Like removed'
            }
            return Response(response_data)
        else:
            post.like.add(current_user)
            post.update_like_count()

            response_data = {
                'status_code' : 6000,
                'message' : 'Post Liked successfully'
            }
            return Response(response_data)

    else:
        response_data = {
            'status_code' : 6001,
            'message': 'Post not found'
        }
        return Response(response_data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment(request, id):
    if Post.objects.filter(pk = id).exists():
        post = Post.objects.get(pk = id)
        comment_text = request.data.get('comment')
        if comment_text:
            current_user = request.user
            saved_comment = Comments.objects.create(
                comment=comment_text,
                user_name=current_user.username
            )
            post.comments.add(saved_comment)
            comment_data = CommentSerializer(saved_comment)

            response_data = {
                'status_code': 6000,
                'message': 'Comment saved successfully',
                'comment': comment_data.data
            }
            return Response(response_data)
        else:
            response_data = {
                'status_code': 6001,
                'message': 'Comment is required'
            }
            return Response(response_data)
    else:
        response_data = {
            'status_code': 6001,
            'message': 'POst not found'
        }
        return Response(response_data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_comment(request, post_id, comment_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return Response({
            'status_code': 6001,
            'message': 'Post not found'
        }, status=status.HTTP_404_NOT_FOUND)

    try:
      
        comment = Comments.objects.get(pk=comment_id)
    except Comments.DoesNotExist:
        return Response({
            'status_code': 6001,
            'message': 'Comment not found'
        }, status=status.HTTP_404_NOT_FOUND)

    if comment.user_name != request.user.username:
        return Response({
            'status_code': 6001,
            'message': 'You are not authorized to delete this comment'
        }, status=status.HTTP_403_FORBIDDEN)

    if comment not in post.comments.all():
        return Response({
            'status_code': 6001,
            'message': 'Comment does not belong to this post'
        }, status=status.HTTP_400_BAD_REQUEST)
    post.comments.remove(comment)
    

    comment.delete()

    return Response({
        'status_code': 6000,
        'message': 'Comment deleted successfully'
    }, status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_comment(request, post_id, comment_id):
    try:
       
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return Response({
            'status_code': 6001,
            'message': 'Post not found'
        }, status=status.HTTP_404_NOT_FOUND)

    try:
  
        comment = Comments.objects.get(pk=comment_id)
    except Comments.DoesNotExist:
        return Response({
            'status_code': 6001,
            'message': 'Comment not found'
        }, status=status.HTTP_404_NOT_FOUND)


    if comment.user_name != request.user.username:
        return Response({
            'status_code': 6001,
            'message': 'You are not authorized to edit this comment'
        }, status=status.HTTP_403_FORBIDDEN)


    if comment not in post.comments.all():
        return Response({
            'status_code': 6001,
            'message': 'Comment does not belong to this post'
        }, status=status.HTTP_400_BAD_REQUEST)


    new_comment_text = request.data.get('comment')

    if new_comment_text:
        comment.comment = new_comment_text
        comment.save()

        comment_data = CommentSerializer(comment)
        return Response({
            'status_code': 6000,
            'message': 'Comment updated successfully',
            'comment': comment_data.data
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            'status_code': 6001,
            'message': 'Comment text is required'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def all_comments(request, id):
    if Post.objects.filter(pk = id).exists():
        post = Post.objects.get(pk = id)
        full_comments = post.comments.all()

        serializer = CommentSerializer(full_comments, many=True)

        response_data = {
            'status_code': 6000,
            'comments': serializer.data
        }
        
        return Response(response_data)
    else:
        response_data = {
            'status_code': 6001,
            'message': 'Post not found'
        }
        return Response(response_data)






