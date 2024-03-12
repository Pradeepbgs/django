from django.db import models
from django.contrib.auth import get_user_model

class ImagePost(models.Model):
    caption = models.CharField(max_length=200)
    image = models.URLField(max_length=500)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,null=True ,default=None)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, default=None)
    post = models.ForeignKey(ImagePost,on_delete=models.CASCADE,null=True,default=None)
    comment = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.comment[:20]}...'
    

class Like(models.Model):
    liked_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(ImagePost, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


