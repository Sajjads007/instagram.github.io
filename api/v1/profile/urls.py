from django.urls import path
from api.v1.profile.views import create_profile, my_profile, update_profile, follow_or_unfollow, followers_list, following_list



urlpatterns = [
    path('create_profile/',create_profile),
    path('my-profile/',my_profile),
    path('update_profile/',update_profile),
    path('follow_or_unfollow/<int:id>/',follow_or_unfollow),
    path('followers/<int:id>/',followers_list),
    path('following/<int:id>/',following_list)
   
]