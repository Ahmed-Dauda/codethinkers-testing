from django.db import models
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from sms.models import Categoriess, Coursess, Topicss, Comments
from django.views.generic import ListView, DetailView, CreateView
# from django.contrib.auth.models import User

# password reset import

from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
# from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib import messages #import messages
# end password reset import.
from django.contrib.auth import get_user_model
User = get_user_model()

from sms.forms import signupform
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
import sweetify
from sms.forms import feedbackform

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sessions.models import Session
# from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone
from hitcount.views import HitCountDetailView

# def get_current_users():
#     active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
#     user_id_list = []
#     for session in active_sessions:
#         data = session.get_decoded()
#         user_id_list.append(data.get('_auth_user_id', None))
#     # Query all logged in users based on id list
#     return User.objects.filter(id__in=user_id_list)



class Categorieslistview(LoginRequiredMixin, ListView):
    models = Categoriess
    template_name = 'sms/home.html'
    success_message = 'TestModel successfully updated!'
    count_hit = True
    queryset = Categoriess.objects.all()
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['students'] = User.objects.all().count()

        # context['category'] = Categories.objects.all().count()
        # context['courses'] = Courses.objects.all().count()
        # num_visit = self.request.session.get('num_visit', 0)
        # self.request.session['num_visit'] = num_visit + 1
        # context['num_visit'] = num_visit
        # context['user_name'] = self.request.user
        # context['current_users'] = get_current_users()
        # context['current_users_count'] = get_current_users().count()
        # context['comment_count'] = Comment.objects.all().count() 
    
        sweetify.success(self.request, 'You successfully changed your password')
        return context



from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('accounts/login')

        
class Courseslistview( HitCountDetailView,LoginRequiredMixin, DetailView):
    models = Categoriess
    template_name = 'sms/courseslistview.html'
    count_hit = True
    queryset = Categoriess.objects.all()

    
        
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['courses'] = Coursess.objects.filter(categories__pk = self.object.id)
        context['courses_count'] = Coursess.objects.filter(categories__pk = self.object.id)

        return context

class Topicslistview( HitCountDetailView,LoginRequiredMixin, DetailView, ):
    models = Coursess
    template_name = 'sms/topicslistview.html'
    count_hit = True
    queryset = Coursess.objects.all()
  
        
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['topics'] = Topicss.objects.filter(courses__pk = self.object.id) 
        context['topics_count'] = Topicss.objects.filter(courses__pk = self.object.id) 
        return context

class Topicsdetailview( HitCountDetailView,LoginRequiredMixin,DetailView):
    models = Topicss
    template_name = 'sms/topicsdetailview.html'
    count_hit = True
    queryset = Topicss.objects.all()
    
        

from sweetify.views import SweetifySuccessMixin

class signupview(SuccessMessageMixin,CreateView):
    
    form_class =signupform
    template_name =  'sms/signup.html'
    success_url = reverse_lazy('sms:signupsuccess')
    success_message = 'TestModel successfully updated!'
    
class Signupsuccess(ListView):
    models = ''
    template_name = 'sms/signupsuccess.html'
    success_url = reverse_lazy('sms:signupview')

    queryset = Comments.objects.all()

class Commentlistview(LoginRequiredMixin, ListView):
    models = Comments
    template_name = 'sms/commentlistview.html'
    queryset = Comments.objects.all()
    
        
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['comments'] = Comments.objects.all() 
        context['user_comment'] = self.request.user
        context['comment_count'] = Comments.objects.all().count() 
        return context

class Commentlistviewsuccess(LoginRequiredMixin, ListView):
    models = Comments
    template_name = 'sms/commentlistviewsuccess.html'
    queryset = Comments.objects.all()
   
        
class Feedbackformview(SuccessMessageMixin,CreateView):
    
    form_class = feedbackform
    template_name =  'sms/feedbackformview.html'
    success_url = reverse_lazy('sms:commentlistviewsuccess')
    success_message = 'TestModel successfully updated!'




# def password_reset_request(request):
# 	if request.method == "POST":
# 		password_reset_form = PasswordResetForm(request.POST)
# 		if password_reset_form.is_valid():
# 			data = password_reset_form.cleaned_data['email']
# 			associated_users = User.objects.filter(Q(email=data))
# 			if associated_users.exists():
# 				for user in associated_users:
# 					subject = "Password Reset Requested"
# 					email_template_name = "main/password/password_reset_email.txt"
# 					c = {
# 					"email":user.email,
# 					# 'domain':'127.0.0.1:8000',
#                     # 'domain':'https://codethinkers.org',
# 					'site_name': 'Website',
# 					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
# 					"user": user,
# 					'token': default_token_generator.make_token(user),
# 					'protocol': 'http',
# 					}
# 					email = render_to_string(email_template_name, c)
# 					try:
# 						send_mail(subject, email, 'smtp.gmail.com' , [user.email], fail_silently=False)
# 					except BadHeaderError:
# 						return HttpResponse('Invalid header found.')
                    
# 					return redirect ("/password_reset/done/")
                    
# 	password_reset_form = PasswordResetForm()
# 	return render(request=request, template_name="main/password/password_reset.html", context={"password_reset_form":password_reset_form})
