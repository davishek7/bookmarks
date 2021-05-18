from django.test import TestCase
from .models import Profile
from django.contrib.auth.models import User

class ProfileTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username = 'abc',password='password')

    def test_profile_created(self):
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.id,1)
        self.assertEqual(profile.__str__(), 'Profile for abc')
