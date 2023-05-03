import pathlib

from django.db import models

from django.dispatch import receiver
from django.db.models.signals import pre_delete, pre_save

from users.models import User

from django.template.defaultfilters import slugify




class Category(models.Model):
    name = models.CharField(null=False, max_length=50)

    class Meta:
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class News(models.Model):
    title = models.CharField(null=False, max_length=100)
    text = models.TextField(null=False)
    date_publication = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='news')
    image = models.ImageField(upload_to="news", null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    in_processing = models.BooleanField(default=True)
    slug = models.SlugField(max_length=100, blank=True, unique=True)

    class Meta:
        verbose_name_plural = 'Новости'
        ordering = ('-date_publication',)

    def __str__(self):
        return self.title


class Comments(models.Model):
    comment = models.CharField(max_length=200, null=True)
    commentator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    date_comment = models.DateTimeField(auto_now_add=True)
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Комментарии'
        ordering = ('date_comment',)




@receiver([pre_save], sender=News)
def create_slug(sender, instance: News, **kwargs):
    instance.slug = slugify(
        instance.title.translate(
            str.maketrans(
                r"абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
                r"abvgdeejzijklmnoprstufhc4ss_y_euaABVGDEEJZIJKLMNOPRSTUFHC4SS_Y_EUA",
            )
        )
    )

# @receiver([pre_delete], sender=News)
# def delete_files(sender, instance: News, **kwargs):
#     file = pathlib.Path(instance.image.path)
#     if not file == "":
#         file.unlink()
