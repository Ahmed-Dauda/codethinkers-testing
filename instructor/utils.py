from .models import InstructorEarning

def split_commission(amount, rate):
    instructor_amount = int(amount * (100 - rate) / 100)
    platform_amount = int(amount * rate / 100)
    return instructor_amount, platform_amount

from .models import InstructorEarning
from sms.models import Courses

def process_course_payment_earnings(payment, course, instructor_user):
    """
    Create InstructorEarning for a single course payment.
    """

    exists = InstructorEarning.objects.filter(
        payment=payment,
        course=course,
        instructor=instructor_user
    ).exists()

    if exists:
        return

    commission_rate = 30.0  # %
    instructor_amount = int(payment.amount * (100 - commission_rate) / 100)
    platform_amount = int(payment.amount - instructor_amount)

    InstructorEarning.objects.create(
        instructor=instructor_user,
        course=course,
        payment=payment,
        amount_paid=payment.amount,
        commission_rate=commission_rate,
        instructor_amount=instructor_amount,
        platform_amount=platform_amount,
        is_paid_out=False
    )


def process_certificate_payment_earnings(cert_payment, instructor_user):
    """
    Create InstructorEarning for a certificate payment.
    `cert_payment` is a CertificatePayment instance.
    `instructor_user` is the instructor's User/NewUser object.
    """

    for course in cert_payment.courses.all():
        # Check if earnings already exist
        exists = InstructorEarning.objects.filter(
            certificate_payment=cert_payment,
            course=course,
            instructor=instructor_user
        ).exists()

        if exists:
            continue

        commission_rate = 30.0
        instructor_amount = int(cert_payment.amount * (100 - commission_rate) / 100)
        platform_amount = int(cert_payment.amount - instructor_amount)

        InstructorEarning.objects.create(
            instructor=instructor_user,
            course=course,
            certificate_payment=cert_payment,
            amount_paid=cert_payment.amount,
            commission_rate=commission_rate,
            instructor_amount=instructor_amount,
            platform_amount=platform_amount,
            is_paid_out=False
        )
