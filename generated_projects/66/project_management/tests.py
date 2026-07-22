from django.test import TestCase
from .models import Project, Owner

class ProjectModelTest(TestCase):
    def setUp(self):
        owner = Owner.objects.create(name='John Doe', email='john@example.com')
        self.project = Project.objects.create(title='Test Project', description='Test Description', deadline='2023-12-31', owner=owner)

    def test_project_str(self):
        self.assertEqual(str(self.project), 'Test Project')