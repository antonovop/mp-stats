from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    id_user = models.IntegerField()
    profile_img = models.ImageField(
        upload_to='profile_images', default='blank profile image.png')
    wb_keywords = models.TextField(blank=True)
    ozon_keywords = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
