from django.test import TestCase
from .models import Student

class StudentModelTest(TestCase):
    def setUp(self):
        Student.objects.create(name='John Doe', ca=30, exam=70)

    def test_total_calculation(self):
        student = Student.objects.get(name='John Doe')
        self.assertEqual(student.total, 100)