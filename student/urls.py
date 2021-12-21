from django.urls import path

# from student.views import views
from student.views import(
    take_exam_view,
      
) 

app_name = 'student'

urlpatterns = [
  
    path('exam', take_exam_view, name='exam'),
   
]




