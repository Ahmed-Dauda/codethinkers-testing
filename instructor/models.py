# earnings/models.py
from django.db import models
from django.contrib.auth import get_user_model
from sms.models import Courses
from student.models import Payment, CertificatePayment

User = get_user_model()

class InstructorEarning(models.Model):
    instructor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='earnings'
    )

    course = models.ForeignKey(
        Courses, on_delete=models.CASCADE
    )

    # Link to original payment
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL,
        null=True, blank=True
    )

    certificate_payment = models.ForeignKey(
        CertificatePayment, on_delete=models.SET_NULL,
        null=True, blank=True
    )

    amount_paid = models.PositiveBigIntegerField()
    commission_rate = models.DecimalField(
        max_digits=5, decimal_places=2, default=30.00
    )

    instructor_amount = models.PositiveBigIntegerField()
    platform_amount = models.PositiveBigIntegerField()

    is_paid_out = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.instructor.email} | {self.course.title} | {self.instructor_amount}"
