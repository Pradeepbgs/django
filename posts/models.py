from django.db import models
from django.contrib.auth import get_user_model

class ImagePost(models.Model):
    file_url = models.URLField(max_length=500)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,null=True ,default=None)
    created_at = models.DateTimeField(auto_now_add=True)






