import requests
import json
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    email = request.data['email']
    user_name = request.data['username']
    password = request.data['password']
    if user_name and password:
        if not User.objects.filter(username = user_name).exists():
            user = User.objects.create_user(
                username = user_name,
                password = password,
                email = email
            )
            headers = {
                'Content-type' : 'application/json'
            }
            protocol = "http://"
            if request.is_secure():
                protocol = "https://"
            host = request.get_host()

            url = protocol + host + "/api/v1/auth/token/"
            
            data = {
                'username' : user_name,
                'password' : password
            }
            response = requests.post(url = url,headers = headers, json = data)
            if response.status_code == 200:
                response_data = {
                    "status_code": 6000,
                    "message": "User successfully created",
                    "response":response.json()
                }
                return Response(response_data)
            else:
                response_data = {
                    "status_code": 6001,
                    "message": "Status code error",
                }
                return Response(response_data)
        else:
            response_data = {
                "status_code" : 6001,
                "message" : "User already exists"
            }

            return Response(response_data)
    else:
        response_data = {
                "status_code" : 6001,
                "message" : "Required Username and Password"
            }

        return Response(response_data)



from django.contrib.auth import authenticate

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    
    user = request.user

    current_password = request.data.get('current_password')
    new_password = request.data.get('new_password')
    confirm_password = request.data.get('confirm_password')


    if not current_password or not new_password or not confirm_password:
        return Response({
            "status_code": 6001,
            "message": "Current password, new password, and confirmation are required."
        })

 
    if new_password != confirm_password:
        return Response({
            "status_code": 6001,
            "message": "New password and confirmation do not match."
        })

    user = authenticate(username=user.username, password=current_password)
    
    if not user:
        return Response({
            "status_code": 6001,
            "message": "Current password is incorrect."
        })
    user.set_password(new_password)
    user.save()

    return Response({
        "status_code": 6000,
        "message": "Password successfully updated."
    })





