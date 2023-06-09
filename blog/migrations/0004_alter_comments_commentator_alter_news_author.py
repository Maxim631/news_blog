# Generated by Django 4.2 on 2023-04-25 17:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0003_rename_uploaded_news_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='commentator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='news',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='news', to=settings.AUTH_USER_MODEL),
        ),
    ]
