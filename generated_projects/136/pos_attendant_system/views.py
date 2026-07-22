from django.views.generic import TemplateView
from .models import PosAttendant, SalesRecord

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_attendants'] = PosAttendant.objects.count()
        context['total_sales'] = SalesRecord.objects.count()
        context['sales_records'] = SalesRecord.objects.select_related('attendant').order_by('-date')
        return context