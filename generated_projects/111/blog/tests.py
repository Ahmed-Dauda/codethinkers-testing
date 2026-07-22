from django.test import TestCase
from .models import Post
from django.contrib.auth import get_user_model

User = get_user_model()

class PostModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.post = Post.objects.create(title='Test Post', content='This is a test post.', author=self.user)

    def test_post_str(self):
        self.assertEqual(str(self.post), 'Test Post')

    def test_post_creation(self):
        self.assertEqual(self.post.content, 'This is a test post.')