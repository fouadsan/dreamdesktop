from django.shortcuts import redirect
from django.contrib import messages
from .models import Product, Category
from .forms import CategoryUpdateForm, ProductUpdateForm
from cryptography.fernet import Fernet


def delete(request, db_table, form_name, _id):
    queryset = (eval(db_table)).objects.get(id=_id)
    if request.user.is_staff and request.method == 'POST' and form_name in request.POST:
        queryset.delete()
        messages.success(request, f'{db_table} Was Successfully Deleted')
        return redirect('main:products')
    else:
        messages.warning(request, 'Deletion failed, You Are Not Allowed To Do That')
        return redirect('main:products')


def update(request, db_table, form_name, form, _id):
    queryset = (eval(db_table)).objects.get(id=_id)
    if request.user.is_staff and request.method == 'POST' and form_name in request.POST:
        form_update = (eval(form))(request.POST, instance=queryset)
        if form_update.is_valid():
            form_update.save()
            messages.success(request, f'{db_table} Was Successfully Updated')
            return redirect('main:products')
    else:
        messages.warning(request, 'Update failed, You Are Not Allowed To Do That')
        return redirect('main:products')


def encrypt(data):
    key = 'mPB25uUObrp0R0B3zJx8Rrh-0iU9SoPNpEUoskFQQI8='
    fernet = Fernet(key)
    token = fernet.encrypt(bytes(str(data), encoding='utf-8'))
    print(token)
    return token


def decrypt(token):
    key = 'mPB25uUObrp0R0B3zJx8Rrh-0iU9SoPNpEUoskFQQI8='
    fernet = Fernet(key)
    original = fernet.decrypt(bytes(str(token), encoding='utf-8'))
    return original.decode()





