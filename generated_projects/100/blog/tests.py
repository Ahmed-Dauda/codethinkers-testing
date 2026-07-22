from django.test import TestCase
from .models import BlogPost

class BlogPostModelTest(TestCase):
    def setUp(self):
        BlogPost.objects.create(title='Test Post', content='This is a test post.')

    def test_blog_post_content(self):
        post = BlogPost.objects.get(id=1)
        expected_object_name = f'{post.title}'
        self.assertEqual(expected_object_name, 'Test Post')