from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from home.models import Setting


def index(request):
    setting= Setting.objects.get(pk=1)
    text="Django Kurulumu: python -m pip installl -e django <br> Proje olusturma: django-admin startproject mysite <br> App Ekleme: python manage.py startapp polls "
    context = {'setting': setting}
    return render(request, 'index.html', context)