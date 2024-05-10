from django.urls import path
from . import views

app_name = 'transaction'

urlpatterns = [
    path('<uuid:book_pk>/checkout/', views.transaction_checkout, name='checkout'),
    path('<uuid:book_pk>/return/', views.start_return_process, name='return'),
    # path('<uuid:book_pk>/return/select_return_transaction',
    #      views.select_return_transaction, name='select_return_transaction'),
    path('return_success/', views.return_success, name='return_success'),
    path('transactions/', views.transaction_list, name='transaction_list')
]
