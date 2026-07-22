from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Student, Teacher, Course, Attendance, DailyShopRecord, LightViolation
from django.db.models import Sum

class HomeView(ListView):
    model = Student
    template_name = 'home.html'
    context_object_name = 'students'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teachers'] = Teacher.objects.all().count()
        context['courses'] = Course.objects.all().count()
        context['violations'] = LightViolation.objects.all().count()
        return context

class StudentListView(ListView):
    model = Student
    template_name = 'student_list.html'
    context_object_name = 'students'
    def get_queryset(self):
        return super().get_queryset().order_by('-id')

class StudentDetailView(DetailView):
    model = Student
    template_name = 'student_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_shop_expenses'] = DailyShopRecord.objects.filter(student=self.object).aggregate(total=Sum('amount_spent'))['total'] or 0
        return context

class StudentCreateView(CreateView):
    model = Student
    template_name = 'student_form.html'
    fields = '__all__'
    success_url = '/students/'

class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'student_form.html'
    fields = '__all__'
    success_url = '/students/'

class TeacherListView(ListView):
    model = Teacher
    template_name = 'teacher_list.html'
    context_object_name = 'teachers'
    def get_queryset(self):
        return super().get_queryset().order_by('-id')

class CourseListView(ListView):
    model = Course
    template_name = 'course_list.html'
    context_object_name = 'courses'
    def get_queryset(self):
        return super().get_queryset().order_by('-id')

class DailyShopRecordListView(ListView):
    model = DailyShopRecord
    template_name = 'shoprecord_list.html'
    context_object_name = 'shop_records'
    def get_queryset(self):
        return super().get_queryset().order_by('-date')

class DailyShopRecordDetailView(DetailView):
    model = DailyShopRecord
    template_name = 'shoprecord_detail.html'

class DailyShopRecordCreateView(CreateView):
    model = DailyShopRecord
    template_name = 'shoprecord_form.html'
    fields = '__all__'
    success_url = '/shoprecords/'

class LightViolationListView(ListView):
    model = LightViolation
    template_name = 'violation_list.html'
    context_object_name = 'violations'
    def get_queryset(self):
        return super().get_queryset().order_by('-id')

class LightViolationDetailView(DetailView):
    model = LightViolation
    template_name = 'violation_detail.html'

class LightViolationCreateView(CreateView):
    model = LightViolation
    template_name = 'violation_form.html'
    fields = '__all__'
    success_url = '/violations/'