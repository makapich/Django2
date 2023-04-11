from django.urls import path

from . import views

app_name = 'celery_example'
urlpatterns = [
    path('reminder', views.reminder, name='reminder'),
    path('success/', views.success_page, name='success-page'),

]