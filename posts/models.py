from django.db import models
from django.contrib.auth import get_user_model

class ImagePost(models.Model):
    caption = models.CharField(max_length=200)
    image = models.URLField(max_length=500)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,null=True ,default=None)
    created_at = models.DateTimeField(auto_now_add=True)
