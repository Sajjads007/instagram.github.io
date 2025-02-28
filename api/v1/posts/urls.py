from django.urls import path
from api.v1.posts.views import posts, delete_post, edit_post, my_post, like, create_post, comment, delete_comment, edit_comment, all_comments


urlpatterns = [
    path('',posts),
    path('create_post/',create_post),
    path('delete/<int:id>/',delete_post),
    path('edit/<int:id>/',edit_post),
    path("my-post/",my_post),
    path('like/<int:id>/',like),
    path('comments/<int:id>/',comment),
    path('<int:post_id>/comments/<int:comment_id>/delete/', delete_comment),
    path('<int:post_id>/comments/<int:comment_id>/edit/', edit_comment),
    path('all_comments/<int:id>/',all_comments)
]