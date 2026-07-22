from django.test import TestCase
from .models import Patient

class PatientModelTest(TestCase):
    def setUp(self):
        Patient.objects.create(first_name='John', last_name='Doe', age=30, gender='Male', address='123 Main St', phone_number='1234567890', email='john@example.com')

    def test_patient_str(self):
        patient = Patient.objects.get(first_name='John')
        self.assertEqual(str(patient), 'John Doe')