from django.test import TestCase
from .models import Employee, Department

class EmployeeModelTest(TestCase):
    def setUp(self):
        department = Department.objects.create(name='HR')
        Employee.objects.create(name='John Doe', email='john@example.com', department=department)

    def test_employee_str(self):
        employee = Employee.objects.get(id=1)
        self.assertEqual(str(employee), 'John Doe')

class DepartmentModelTest(TestCase):
    def setUp(self):
        Department.objects.create(name='IT')

    def test_department_str(self):
        department = Department.objects.get(id=1)
        self.assertEqual(str(department), 'IT')