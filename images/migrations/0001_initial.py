# Generated by Django 3.2 on 2021-05-04 05:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import images.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200)),
                ('slug', models.SlugField(blank=True, max_length=200)),
                ('url', models.URLField()),
                ('image', models.ImageField(blank=True, upload_to=images.models.user_directory_path)),
                ('description', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='images_created', to=settings.AUTH_USER_MODEL)),
                ('users_like', models.ManyToManyField(blank=True, related_name='image_liked', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]