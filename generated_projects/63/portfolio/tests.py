from django.test import TestCase
from .models import Project, Skill, Experience

class ProjectModelTest(TestCase):
    def setUp(self):
        Project.objects.create(title='Test Project', description='Test Description', url='http://test.com')

    def test_project_str(self):
        project = Project.objects.get(id=1)
        self.assertEqual(str(project), 'Test Project')