from django.db import models

class ImagePost(models.Model):
    caption = models.CharField(max_length=200)
    image = models.ImageField(upload_to='public/temp/')
    created_at = models.DateTimeField(auto_now_add=True)
