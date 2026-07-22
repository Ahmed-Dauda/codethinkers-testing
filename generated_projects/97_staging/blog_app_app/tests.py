from django.test import TestCase
from .models import BlogPost

class BlogPostModelTest(TestCase):
    def setUp(self):
        BlogPost.objects.create(title='Test Post', content='Test Content')

    def test_blog_post_creation(self):
        post = BlogPost.objects.get(title='Test Post')
        self.assertEqual(post.content, 'Test Content')