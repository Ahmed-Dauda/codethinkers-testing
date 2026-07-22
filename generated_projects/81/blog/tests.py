from django.test import TestCase
from .models import Post, Category

class PostModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.post = Post.objects.create(title='Test Post', content='Test Content', category=self.category)

    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.category.name, 'Test Category')