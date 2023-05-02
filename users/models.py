from django.db import models
import pathlib
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_delete
from django.dispatch import receiver


class User(AbstractUser):
    user_picture = models.ImageField(upload_to="user_picture",
                                     null=True,
                                     blank=True
                                     )

    class Meta:
        db_table = "user"
        verbose_name_plural = 'Пользователи'





@receiver([pre_delete], sender=User)
def delete_files(sender, instance: User, **kwargs):
    file = pathlib.Path(instance.user_picture.path)
    file.unlink()
