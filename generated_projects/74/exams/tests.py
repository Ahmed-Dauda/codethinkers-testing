from django.test import TestCase
from .models import Exam

class ExamModelTest(TestCase):
    def setUp(self):
        Exam.objects.create(title='Math Exam', date='2023-05-01', duration='01:00:00', total_marks=100, description='Final math exam.')

    def test_exam_creation(self):
        exam = Exam.objects.get(title='Math Exam')
        self.assertEqual(exam.total_marks, 100)