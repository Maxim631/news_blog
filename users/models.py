from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    user_picture = models.ImageField(upload_to="user_picture",
                                     null=True,
                                     blank=True,
                                     default='not_user/not_user.jpg')

    class Meta:
        db_table = "user"
