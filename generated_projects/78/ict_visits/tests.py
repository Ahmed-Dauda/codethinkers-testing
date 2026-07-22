from django.test import TestCase
from .models import StudentVisit

class StudentVisitModelTest(TestCase):
    def setUp(self):
        StudentVisit.objects.create(student_name='John Doe', visit_time='2023-10-01 10:00:00', purpose='Consultation')

    def test_student_visit_str(self):
        visit = StudentVisit.objects.get(id=1)
        self.assertEqual(str(visit), 'John Doe')