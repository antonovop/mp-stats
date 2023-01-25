from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    id_user = models.TextField()
    profile_img = models.ImageField(
        upload_to='profile_images', default='blank profile image.png')
    # list of products that user has chosen for tracking
    # for simplicity, let's store it as a string
    ozon_products = models.TextField(blank=True)
    wb_products = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


# class Product(models.Model):
#    # unique id because article can be repeated
#    id_product = models.IntegerField()
#    article_number = models.IntegerField()
#    keywords = models.TextField()
