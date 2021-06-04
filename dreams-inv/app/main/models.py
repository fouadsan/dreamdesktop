from django.contrib import admin
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File
import string
import secrets
from django.core.validators import MinLengthValidator


class Company(models.Model):
    name = models.CharField(max_length=50, validators=[MinLengthValidator(limit_value=3,
                                                                          message="Name must be 3 characters at least")]
                            )
    logo = models.ImageField(upload_to='images/company/', blank=True)

    class Meta:
        verbose_name = 'company'
        verbose_name_plural = 'company'


class Category(models.Model):
    name = models.CharField(max_length=50, db_index=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-created_at', )
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class ProductDataModel(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    buying_price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    unit_price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    quantity = models.IntegerField(default='0', blank=True, null=True)
    received_quantity = models.IntegerField(default='0', blank=True,
                                            null=True)
    received_by = models.CharField(max_length=50, blank=True, null=True)
    issued_quantity = models.IntegerField(default='0', blank=True, null=True)
    issued_by = models.CharField(max_length=50, blank=True, null=True)
    issued_to = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT)
    reorder_level = models.IntegerField(default='0', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.name + ' ' + str(self.quantity)

    class Meta:
        abstract = True


class Product(ProductDataModel):
    pass

    class Meta:
        ordering = ('-created_at',)


class ProductHistory(ProductDataModel):
    pass

    class Meta:
        verbose_name = 'product history'
        verbose_name_plural = 'products history'


class CustSup(models.Model):
    name = models.CharField(max_length=50, unique=True)
    address = models.CharField(max_length=120, blank=True)
    phone = PhoneNumberField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='created_by')
    updated_by = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='updated_by')
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)


class Customer(CustSup):
    pass

    def __str__(self):
        return self.name


class Supplier(CustSup):
    pass

    def __str__(self):
        return self.name


class Barcode(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.RESTRICT, blank=True, null=True, default=1)
    barcode_digit = models.CharField(max_length=13, blank=True, null=True)
    barcode_img = models.ImageField(upload_to='images/barcodes/', blank=True)
    # country_id = models.CharField(max_length=1, null=True)
    # manufacturer_id = models.CharField(max_length=6, null=True)
    # number_id = models.CharField(max_length=5, null=True)

    def save(self, *args, **kwargs):
        alphabet = string.ascii_letters + string.digits
        code = f'{self.company.name[:3]}' + ''.join(secrets.choice(alphabet) for i in range(9))
        print(code)
        code_39 = barcode.get_barcode_class('code39')
        code39_digit = code_39(code)
        self.barcode_digit = code39_digit
        code39_image = code_39(code, writer=ImageWriter())
        buffer = BytesIO()
        code39_image.write(buffer)
        self.barcode_img.save(f'{self.product}_code.png', File(buffer), save=False)
        return super().save(*args, **kwargs)
