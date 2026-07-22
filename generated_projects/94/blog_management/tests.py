from django.test import TestCase
from .models import Post, Category

class PostModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.post = Post.objects.create(title='Test Post', content='Test Content', category=self.category)

    def test_post_str(self):
        self.assertEqual(str(self.post), 'Test Post')

    def test_category_str(self):
        self.assertEqual(str(self.category), 'Test Category')