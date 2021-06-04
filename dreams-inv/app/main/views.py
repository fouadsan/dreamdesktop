from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Product, Category, Company
from .forms import CategoryCreateForm, ProductCreateForm
from .utils import delete, update, encrypt, decrypt
from .resources import ProductResource
from tablib import Dataset


company_data = Company.objects.all()[:1]
glob_context = {
    'company_data': company_data
}


@login_required
def home(request):

    context = {
        'nbar': 'home',
    }
    context.update(glob_context)
    return render(request, 'main/index.html', context)


@login_required
def products(request):
    categories = Category.objects.all()
    queryset = Product.objects.all()
    form_create_cat = CategoryCreateForm()

    # Create category
    if request.method == 'POST' and 'create_cat' in request.POST:
        form_create_cat = CategoryCreateForm(request.POST)
        if form_create_cat.is_valid():
            form_create_cat.save()
            messages.success(request, 'Successfully Created')
            return redirect('/products')
        else:
            form_name_data = form_create_cat['name'].value()
            if Category.objects.filter(name=form_name_data):
                messages.warning(request, 'Creation failed, Category already exists')

            else:
                messages.warning(request, 'Creation failed')
                return redirect('/products')
            # print (form_create['name'].value())

    #Create product
    form_create_prod = ProductCreateForm()
    if request.method == 'POST' and 'create_prod' in request.POST:
        form_create_prod = ProductCreateForm(request.POST)
        if form_create_prod.is_valid():
            instance = form_create_prod.save(commit=False)
            instance.created_by = request.user
            instance.save()
            messages.success(request, 'Product Was Successfully Created')
            return redirect('/products')
        else:
            form_name_data = form_create_prod['name'].value()
            if Product.objects.filter(name=form_name_data):
                messages.warning(request, 'Creation failed, Product already exists')
                return redirect('/products')
            else:
                messages.warning(request, 'Creation failed')
                return redirect('/products')
            # print (form_create['name'].value())

    paginator = Paginator(queryset, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'nbar': 'products',
        'categories': categories,
        'queryset': queryset,
        'page_obj': page_obj,
        'form_create_cat': form_create_cat,
        'form_create_prod': form_create_prod
    }
    context.update(glob_context)

    return render(request, 'main/products.html', context)


@login_required
def delete_category(request, _id):
    delete(request, 'Category', 'delete_cat', _id)
    return redirect('main:products')


@login_required
def update_category(request, _id):
    update(request, 'Category', 'update_cat', 'CategoryUpdateForm', _id)
    return redirect('main:products')


@login_required
def delete_product(request, _id):
    delete(request, 'Product', 'delete_prod', _id)
    return redirect('main:products')


@login_required
def update_product(request, _id):
    update(request, 'Product', 'update_prod', 'ProductUpdateForm', _id)
    return redirect('main:products')


@login_required
def delete_products(request):
    if request.user.is_staff and request.method == 'POST' and 'delete_selected_prod' in request.POST:
        queryset = request.POST.getlist('product')
        if queryset:
            Product.objects.filter(pk__in=queryset).delete()
            messages.success(request, 'Selected Products Was Successfully Deleted')
            return redirect('main:products')
        else:
            messages.warning(request, 'No product selected')
            return redirect('main:products')
    else:
        messages.warning(request, 'Deletion failed, You Are Not Allowed To Do That')
        return redirect('main:products')


@login_required
def export_csv(request):
    # export to csv
    if request.method == 'GET' and 'export_csv' in request.GET:
        product_resource = ProductResource()
        dataset = product_resource.export()
        response = HttpResponse(encrypt(dataset.csv), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="products_staff.csv"'
        return response

        # response = HttpResponse(content_type='text/csv')
        # print(response)
        # response['Content-Disposition'] = 'attachment; filename="products_emp.csv"'
        # writer = csv.writer(response)
        # writer.writerow(['#', 'PRODUCT', 'CATEGORY', 'BUYING PRICE', 'UNIT SOLD', 'IN STOCK'])
        # instance = queryset
        # for product in instance:
        #     writer.writerow([product.id, product.name, product.category, product.buying_price, product.unit_price,
        #                      product.quantity])
        # return response
        # return redirect('main:products')


@login_required
def import_csv(request):
    # import from csv
    if request.method == 'POST':
        product_resource = ProductResource()
        dataset = Dataset()
        print(dataset)
        new_products = request.FILES['file']
        imported_data = dataset.load(decrypt(new_products.read().decode()), format='csv')
        print(imported_data)
        result = product_resource.import_data(imported_data, dry_run=True)  # Test the data import
        print(result)
        if not result.has_errors():
            product_resource.import_data(imported_data, dry_run=False)  # Actually import now
            messages.success(request, 'File Imported Successfully')
        else:
            messages.warning(request, 'Could Not Import File')
        return redirect('main:products')


@login_required
def customers(request):
    context = {
        'nbar': 'customers',
    }
    context.update(glob_context)
    return render(request, 'main/customers.html', context)
