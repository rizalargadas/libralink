from django.urls import path
from . import views

app_name = 'patron'

urlpatterns = [
    path('', views.patron_list, name='patron_list'),
    path('add/', views.add_patron, name='add_patron'),
    path('<uuid:pk>/', views.patron_detail, name='patron_detail'),
    path('<uuid:pk>/edit/', views.edit_patron, name='edit_patron'),
    path('<uuid:pk>/deactivate/', views.deactivate_patron,
         name='deactivate_patron'),
]
