from django.test import TestCase
from .models import BlogPost
from django.contrib.auth.models import User

class BlogPostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.post = BlogPost.objects.create(title='Test Post', content='Test Content', author=self.user)

    def test_blog_post_creation(self):
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.content, 'Test Content')
        self.assertEqual(self.post.author.username, 'testuser')