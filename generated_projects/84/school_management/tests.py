from django.test import TestCase
from .models import Student, Teacher, Course

class StudentModelTest(TestCase):
    def setUp(self):
        self.student = Student.objects.create(name='John Doe', age=15, grade='10')

    def test_student_str(self):
        self.assertEqual(str(self.student), 'John Doe')

class TeacherModelTest(TestCase):
    def setUp(self):
        self.teacher = Teacher.objects.create(name='Jane Smith', subject='Mathematics')

    def test_teacher_str(self):
        self.assertEqual(str(self.teacher), 'Jane Smith')