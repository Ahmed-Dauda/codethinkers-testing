from django.test import TestCase
from .models import Patient

class PatientModelTest(TestCase):
    def setUp(self):
        Patient.objects.create(first_name='John', last_name='Doe', date_of_birth='1990-01-01', email='john@example.com', phone='1234567890', address='123 Main St')

    def test_patient_str(self):
        patient = Patient.objects.get(id=1)
        self.assertEqual(str(patient), 'John Doe')