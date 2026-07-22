from django.test import TestCase
from .models import Student

class StudentModelTest(TestCase):
    def setUp(self):
        Student.objects.create(name='John Doe', age=20, enrollment_date='2023-01-01')

    def test_student_creation(self):
        student = Student.objects.get(name='John Doe')
        self.assertEqual(student.age, 20)
        self.assertEqual(str(student), 'John Doe')