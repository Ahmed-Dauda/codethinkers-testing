from django.test import TestCase
from .models import Student, Class, Teacher

class StudentModelTest(TestCase):
    def setUp(self):
        self.class1 = Class.objects.create(name='Math')
        self.student = Student.objects.create(first_name='John', last_name='Doe', email='john@example.com', class_enrolled=self.class1)

    def test_student_str(self):
        self.assertEqual(str(self.student), 'John Doe')