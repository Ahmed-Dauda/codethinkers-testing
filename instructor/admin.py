from django.contrib import admin
from .models import InstructorEarning


@admin.register(InstructorEarning)
class InstructorEarningAdmin(admin.ModelAdmin):
    list_display = (
        'instructor',
        'course',
        'payment',
        'certificate_payment',
        'amount_paid',
        'commission_rate',
        'instructor_amount',
        'platform_amount',
        'is_paid_out',
        'created',
    )

    list_filter = ('is_paid_out', 'created')

    search_fields = (
        'instructor__username',
        'instructor__email',
        'course__title',
        'payment__id',
        'certificate_payment__id',
    )

    readonly_fields = (
        'amount_paid',
        'instructor_amount',
        'platform_amount',
        'created',
    )
