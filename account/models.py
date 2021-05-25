from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


def user_directory_path(instance, filename):
    return f"profile_pic/{instance.user.username}/{filename}"


class Profile(models.Model):

    user = models.OneToOneField(User,blank=True,on_delete = models.CASCADE)

    date_of_birth=models.DateField(blank = True, null = True)

    photo = models.ImageField(upload_to=user_directory_path,default='profile_pic.png', blank=True)


    def __str__(self):
        return f'Profile for {self.user}'


class Contact(models.Model):
    user_from = models.ForeignKey(User,
                                  related_name='rel_from_set',
                                  on_delete=models.CASCADE)
    user_to = models.ForeignKey(User,
                                related_name='rel_to_set',
                                on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'


# Add following field to User dynamically
User.add_to_class('following',
                  models.ManyToManyField('self',through=Contact,related_name='followers',symmetrical=False))
        
