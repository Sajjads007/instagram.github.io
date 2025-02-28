#about
 
following, unfollowing, like, unlike, POstManagement, like and comment management api will only work after you created a UserAccount(CreateProfile)


#set up


#Authentication & Profile Management
		User Registration -  http://127.0.0.1:8000/api/v1/auth/register/
		Login & Logout -  http://127.0.0.1:8000/api/v1/auth/token/
		CreateProfile -   http://127.0.0.1:8000/api/v1/auth/profile/create_profile/
		Update Profile -  http://127.0.0.1:8000/api/v1/auth/profile/update_profile/(PUT)
		Follow/Unfollow Users -  http://127.0.0.1:8000/api/v1/auth/profile/follow_or_unfollow/<id>/ (id of the profile created in CreateProfile)
		FollowersList -  http://127.0.0.1:8000/api/v1/auth/profile/followers/<id>/ (id of the profile created in CreateProfile)
		FollowingList -   http://127.0.0.1:8000/api/v1/auth/profile/following/<id>/ (id of the profile created in CreateProfile)
		Change Password -  http://127.0.0.1:8000/api/v1/auth/change_password/


#Post Management
		Create New Posts -   http://127.0.0.1:8000/api/v1/posts/create_post/
		Edit post -  http://127.0.0.1:8000/api/v1/posts/edit/<id>/ (id of the post)
		Delete Own Posts -  http://127.0.0.1:8000/api/v1/posts/delete/<id>/ (id of the post)
		View All Posts -   http://127.0.0.1:8000/api/v1/posts/ 
		View own post -	 http://127.0.0.1:8000/api/v1/posts/my-post/


#Like & Comment System
		Like/Unlike Posts -   http://127.0.0.1:8000/api/v1/posts/like/<id>/ (id of the post)
		View Number of Likes on a Post -  http://127.0.0.1:8000/api/v1/posts/ (the like_count field will display the count of like)
		Comment on a Post -  http://127.0.0.1:8000/api/v1/posts/comments/<id>/ (id of the post to put comment)
		Edit-comment -  http://127.0.0.1:8000/api/v1/posts/<post_id>/comments/<comment_id>/edit/ (post_id = id of the post to edit comment, comment_id = id of the comment to edit)
		Delete Own Comments -  http://127.0.0.1:8000/api/v1/posts/<int:post_id>/comments/<int:comment_id>/delete/ (post_id = id of the post to delete comment, comment_id = id of the comment to delete)
		View All Comments on a Post - http://127.0.0.1:8000/api/v1/posts/all_comments/<int:id>/ (id of the post)
		
		
		

		
