from django.db import models



class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete = models.CASCADE, related_name = 'userprofile')
    
    def __str__(self):
        return self.user.username

class UserAccount(models.Model):
    user = models.CharField(max_length = 255)       
    name = models.CharField(max_length = 255)
    profile_picture = models.FileField(upload_to = 'profile/image')
    bio = models.CharField(max_length = 225)
    followers = models.ManyToManyField('self', related_name='user_followers', symmetrical=False, blank = True)
    following = models.ManyToManyField('self', related_name='user_following', symmetrical=False, blank = True)

    def __str__(self):
        return self.user


class Post(models.Model):
    image = models.FileField(upload_to='posts/images')
    user_name = models.CharField(max_length = 255)
    caption = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)
    like = models.ManyToManyField('posts.UserAccount', blank=True, related_name='liked_post')
    comments = models.ManyToManyField('posts.Comments', blank=True)
    like_count = models.IntegerField(default=0) 

    def __str__(self):
        return self.caption

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def update_like_count(self):
        self.like_count = self.like.count() 
        self.save() 


class Comments(models.Model):
    user_name = models.CharField(max_length = 255)
    comment = models.CharField(max_length = 255)
    is_deleted = models.BooleanField(default = False)

    def __str__(self):
        return self.user_name


