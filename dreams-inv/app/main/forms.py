from django import forms
from .models import *
from crispy_forms.helper import FormHelper


class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class CategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class ProductCreateForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'category', 'buying_price', 'unit_price', 'quantity', 'reorder_level']

    def clean_category(self):
        category = self.cleaned_data.get('category')
        return category

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError('This field is required')
        return name

    def __init__(self, *args, **kwargs):
        super(ProductCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'buying_price', 'unit_price', 'quantity', 'reorder_level']
