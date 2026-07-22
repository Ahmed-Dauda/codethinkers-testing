from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Staff, Attendance, PerformanceReview

class StaffListView(ListView):
    model = Staff
    template_name = 'staff_list.html'
    paginate_by = 25

    def get_queryset(self):
        return super().get_queryset().order_by('-id')

class StaffDetailView(DetailView):
    model = Staff
    template_name = 'staff_detail.html'

class AttendanceListView(ListView):
    model = Attendance
    template_name = 'attendance_list.html'
    paginate_by = 25

    def get_queryset(self):
        return super().get_queryset().select_related('staff').order_by('-id')

class AttendanceDetailView(DetailView):
    model = Attendance
    template_name = 'attendance_detail.html'

class PerformanceReviewListView(ListView):
    model = PerformanceReview
    template_name = 'performance_review_list.html'
    paginate_by = 25

    def get_queryset(self):
        return super().get_queryset().select_related('staff').order_by('-id')

class PerformanceReviewDetailView(DetailView):
    model = PerformanceReview
    template_name = 'performance_review_detail.html'