
from django.forms import ModelForm
from student.models import Payment

from django import forms
from .models import Payment

from django import forms
from student.models import Order

class CheckoutForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['total_amount', 'payment_reference',]


