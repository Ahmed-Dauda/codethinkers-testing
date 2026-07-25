from webprojects.models import File

# Update views
f = File.objects.get(project_id=70, name='student_records/views.py')
old = "def home(request):\n    return render(request, 'home.html')"
new = "def home(request):\n    students = Student.objects.all().order_by('-id')\n    return render(request, 'list.html', {'objects': students})"
f.content = f.content.replace(old, new)

if 'def student_list' not in f.content:
    f.content += '\n\ndef student_list(request):\n    students = Student.objects.all().order_by(\"-id\")\n    return render(request, \"list.html\", {\"objects\": students})\n'
f.save()
print('Views updated')

u = File.objects.get(project_id=70, name='student_records/urls.py')
u.content = u.content.replace(
    "path('', views.home, name='home'),",
    "path('', views.home, name='home'),\n    path('list/', views.student_list, name='student_list'),"
)
u.save()
print('URLs updated')
