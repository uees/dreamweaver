from django.urls import path

from . import views

app_name = 'sar'
urlpatterns = [
    path('<table_id>/', views.sar, name='table'),
]
