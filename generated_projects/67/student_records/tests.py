from django.test import TestCase
from .models import Student

class StudentModelTest(TestCase):
    def setUp(self):
        Student.objects.create(full_name='John Doe', admission_number='A123', class_name='10A', gender='Male', date_of_birth='2005-05-15', parent_phone='1234567890')

    def test_student_creation(self):
        student = Student.objects.get(admission_number='A123')
        self.assertEqual(student.full_name, 'John Doe')