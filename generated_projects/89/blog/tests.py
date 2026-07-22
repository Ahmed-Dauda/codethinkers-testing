from django.test import TestCase

class BlogTests(TestCase):
    def test_blog_creation(self):
        response = self.client.post('/posts/new/', {'title': 'Test Post', 'content': 'Test Content'})
        self.assertEqual(response.status_code, 302)  # Check for redirect after creation