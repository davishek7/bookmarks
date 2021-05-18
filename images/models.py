from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


def user_directory_path(instance, filename):
    return f"{instance.user}/uploaded_images/{filename}"
    
class Image(models.Model):
    user = models.ForeignKey(User, blank=True,on_delete=models.CASCADE, related_name='images_created')
    title = models.CharField(max_length=200,blank=True)
    slug = models.SlugField(max_length=200,blank=True)
    url = models.URLField()
    image = models.ImageField(upload_to=user_directory_path,blank=True)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True,db_index=True)
    users_like = models.ManyToManyField(User,related_name='image_liked',blank=True)

    class Meta:
        ordering=['-created']

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('images:detail', args=[self.id, self.slug])
