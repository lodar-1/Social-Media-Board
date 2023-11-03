from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint

class User(AbstractUser):
    pass
    
class Post(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="PostUser")
	content = models.CharField(max_length=500)
	post_date = models.DateTimeField(auto_now_add=True, blank=True)

	def serialize(self):
		return {
			"user": self.user_id,
			"date": self.post_date,
			"content": self.content
		}
	# ~ def __str__(self):
		# ~ return f"{self.user} {self.post_date}: {self.content}"	

class Likes(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="LikesUser")
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="PostLike")
	class Meta:
		constraints = [
		UniqueConstraint('user', 'post', name='LikesComposite')]
			
class Follow(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="FollowedUser")
	following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="FollowsUser") 		
	
	def __str__(self):
		return f"{self.user} {self.following}"
