from django.urls import path
from .views import home, products, delete_category, update_category,\
    delete_product, update_product, delete_products, export_csv,\
    import_csv, customers

app_name = 'main'

urlpatterns = [
    path('', home, name='home'),
    path('products/', products, name='products'),
    path('products/category/delete/<int:_id>', delete_category, name='delete_category'),
    path('products/category/update/<int:_id>', update_category, name='update_category'),
    path('products/delete/<int:_id>', delete_product, name='delete_product'),
    path('products/update/<int:_id>', update_product, name='update_product'),
    path('products/delete/', delete_products, name='delete_products'),
    path('products/export/', export_csv, name='export_csv'),
    path('products/import/', import_csv, name='import_csv'),
    path('customers/', customers, name='customers'),
]
