from django.urls import path

from . import views

urlpatterns = [
    # ex: /home/
    path('', views.index, name='index'),
    path('rentproduct/<int:id>/', views.rentproduct, name='rentproduct'),
    # ex: /polls/5/
    #path('<int:question_id>/', views.detail, name='detail'),

]