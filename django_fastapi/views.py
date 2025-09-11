from django.shortcuts import render

def frontend(request):
    return render(request, "django_fastapi/frontend.html")
