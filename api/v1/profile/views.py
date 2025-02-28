from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from posts.models import UserAccount
from api.v1.posts.serializer import UserAccountSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_profile(request):
    name = request.data.get('name')
    profile_picture = request.data.get('picture')
    bio = request.data.get('bio')
    if name and profile_picture:
        if not UserAccount.objects.filter(user = request.user).exists():
            user = UserAccount.objects.create(
                name = name,
                profile_picture = profile_picture,
                bio = bio,
                user = request.user
            )
            response_data = {
                "status_code": 6000,
                "message": "Profile successfully created"
            }
            return Response(response_data)
        else:
            response_data = {
                "status_code": 6001,
                "message": "You already have a profile"
            }
    else:
        response_data = {
            "status_code" : 6001,
            "message" : "Profile name and picture are required"
        }
        return Response(response_data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    if UserAccount.objects.filter(user = request.user).exists():
        profile = UserAccount.objects.get(user = request.user)
        if profile:
            serializer = UserAccountSerializer(profile, data = request.data, partial = True)

            if serializer.is_valid():
                serializer.save()

                response_data = {
                    'status_code': 6000,
                    'message':'profile updated successfully'
                }
                return Response(response_data)
            else:
                response_data = {
                    "status_code" : 6001,
                    "message" : "Invalid data"
                }
        else:
            response_data = {
                "status_code" : 6001,
                "message" : "Profile not found"
            }
    else:
        response_data = {
            "status_code" : 6001,
            "message" : "You don't have a profile"
        }


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_profile(request):
    profile = UserAccount.objects.get(user=request.user)
    if profile:
        serializer = UserAccountSerializer(profile, context = {'request': request})
        response_data = {
            'status_code': 6000,
            'data': serializer.data
        }
        return Response(response_data)
    else:
        response_data = {
            'status_code': 6001,
            'message': 'You do not have a profile'
        }
        return Response(response_data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def follow_or_unfollow(request,id):
    if UserAccount.objects.filter(pk = id).exists():
        profile = UserAccount.objects.get(pk = id)
        current_user = UserAccount.objects.get(user = request.user)
        if current_user not in profile.followers.all():
            profile.followers.add(current_user)
            current_user.following.add(profile)
            response_data = {
                'status_code': 6000,
                'message': 'Successfully Followed'
            }
            return Response(response_data)
        else:
            profile.followers.remove(current_user)
            current_user.following.remove(profile)
            response_data = {
                'status_code': 6000,
                'message': 'Successfully Unfollowed'
            }
            return Response(response_data)
    else:
        response_data = {
            'status_code': 6001,
            'message': 'Profile not found'
        }
        return Response(response_data)


@api_view(["GET"])
@permission_classes([AllowAny])
def followers_list(request,id):
    context = {
        "request":request
    }
    if UserAccount.objects.filter(pk = id).exists():
        profile = UserAccount.objects.get(pk = id)
        list_of_followers = profile.followers.all()
        serializer = UserAccountSerializer(list_of_followers, many = True, context = context)
        
        response_data = {
            'status' : 6000,
            'followers' : serializer.data
        }
        return Response(response_data)
    else:
        response_data = {
            'status' : 6001,
            'message' : 'Profile not found'
        }
        return Response(response_data)


@api_view(['GET'])
@permission_classes([AllowAny])
def following_list(request,id):
    context = {
        "request":request
    }
    if UserAccount.objects.filter(pk = id).exists():
        profile = UserAccount.objects.get(pk = id)
        list_of_following = profile.following.all()
        serializer = UserAccountSerializer(list_of_following, many = True, context = context)
        
        response_data = {
            'status' : 6000,
            'following' : serializer.data
        }
        return Response(response_data)
    else:
        response_data = {
            'status' : 6001,
            'message' : 'Profile not found'
        }
        return Response(response_data)







    
    






