from django.test import TestCase
from .models import Image
from django.conf import settings
from django.contrib.auth.models import User


class ImageTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username = 'abc',password='password')
        Image.objects.create(title='image',slug='image',url='google.com',description='image',user=self.user)
    
    def test_image_created(self):
        image = Image.objects.create(
            title='image1', slug='image1', url='google.com', description='image1', user=self.user)
        self.assertEqual(image.id,2)
        self.assertEqual(image.user,self.user)
        self.assertEqual(image.__str__(),'image1')
