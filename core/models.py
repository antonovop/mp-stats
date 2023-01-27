import json
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    id_user = models.IntegerField()
    profile_img = models.ImageField(
        upload_to='profile_images', default='blank profile image.png')
    ozon_products = models.TextField(default='[]')
    wb_products = models.TextField(default='[]')

    def list_to_string(self, lst):
        return json.dumps(lst)

    def string_to_json(self, s_lst):
        return json.loads(s_lst)

    # storage is ither ozon_products or wb_products
    def fill_storage_wb(self, item):
        # storage is a text field aka string
        # item is a list that represents one item
        storage_lst = self.string_to_json(self.wb_products)
        storage_lst.append(item)
        self.wb_products = self.list_to_string(storage_lst)

    def fill_storage_ozon(self, item):
        storage_lst = self.string_to_json(self.ozon_products)
        storage_lst.append(item)
        self.ozon_products = self.list_to_string(storage_lst)

    def __str__(self):
        return self.user.username


#   class Product(models.Model):
#       id = models.ForeignKey(Profile, on_delete=models.# CASCADE)
#       code = models.ForeignKey(User, on_delete=models.#  CASCADE)
#       keywords = models.TextField(blank=True)
#
