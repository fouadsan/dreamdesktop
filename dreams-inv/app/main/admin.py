from django.contrib import admin
from .models import Company, Category, Product, ProductHistory, Customer, Supplier, Barcode
from import_export.admin import ImportExportModelAdmin


# class ProductAdmin(admin.ModelAdmin):
#     exclude = ('barcode',)
# admin.site.register(Product, ProductAdmin)

admin.site.register(Company)
admin.site.register(Category)
admin.site.register(Barcode)
admin.site.register(ProductHistory)
admin.site.register(Customer)
admin.site.register(Supplier)


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    pass


