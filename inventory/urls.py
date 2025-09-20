from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('pieces/', views.pieces_list, name='pieces_list'),
    path('piece/add/', views.piece_add, name='piece_add'),
    path('transaction/add/', views.transaction_add, name='transaction_add'),
    path('export/', views.export_stock, name='export_stock'),
    path('api/pieces/', views.api_pieces, name='api_pieces'),  # JSON pour DataTables
    path('import-stock/', views.import_stock, name='import_stock'),

]
