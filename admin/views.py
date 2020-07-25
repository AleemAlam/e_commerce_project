from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from django.contrib.auth import login,logout,authenticate
from product.models import Item, Rating, Cart, Order, Category, Payments
from product.forms import ItemForm, CategoryForm
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
# Create your views here.

def admin(request):
    if request.user.is_authenticated and request.user.is_superuser:
        product_count = Item.objects.all().count()
        user_count = User.objects.filter(is_staff=False).count()
        total_product_sales = Order.objects.filter(ordered = True).count()
        recent_corders = Order.objects.filter(ordered = True)
        payments = Payments.objects.all()

        context = {
            'product_count':product_count,
            'user_count':user_count,
            'total_product_sales':total_product_sales,
            'recent_orders':recent_corders,
            'payments': payments
        }
        return render(request, "admin/dashboard.html", context)
    else:
        return redirect('admin_login')

@login_required
def product_list(request):
    object_list = Item.objects.all()
    form = ItemForm()
    form_category = CategoryForm()
    categories = Category.objects.all()
    if 'product' in request.GET:
        product_name = request.GET['product']
        if product_name:
            object_list = Item.objects.filter(title__iexact = product_name)
    return render(request, 'admin/products.html', {'object_list': object_list, 'categories':categories, 'form':form, 'form_category':form_category})

@login_required
def user_list(request):
    object_list = User.objects.all()
    if 'user' in request.GET:
        username = request.GET['user']
        if username:
            object_list = User.objects.filter(username__iexact = username)
    return render(request, 'admin/users.html', {'object_list': object_list})


def admin_login(request):
    if request.user.is_superuser:
        return redirect('admin_dashboad')
    else:
        if request.method == 'POST':
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            if user is None:
                messages.error(request, 'Invalid User')
                return render(request, 'admin/admin_login.html', {'form': AuthenticationForm(),})
            if user.is_superuser:
                login(request, user)
                return redirect('admin_dashboad')
            else:
                messages.error(request, "You are not Authorize to access with this account")
                return render(request, 'admin/admin_login.html', {'form': AuthenticationForm(),})
        else:
            
            return render(request, 'admin/admin_login.html', {'form': AuthenticationForm(),})


@login_required
def product_details(request, pk):
    product = get_object_or_404(Item, pk = pk)
    final_price = product.price - product.discount_price
    form = ItemForm(instance=product)
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            if form.cleaned_data['image']:
                product.image = form.cleaned_data['image']
            else:
                product.image = form.cleaned_data['old_image']
            product.save()
            messages.info(request, "Product Updated")
            return render(request, 'admin/product_details.html', {'product': product, 'final_price': final_price})
        else:
            messages.error(request, "Please Enter Valid Details")
    return render(request, 'admin/product_details.html', {'product': product, 'final_price': final_price, 'form': form})


@login_required
def admin_logout(request):
    logout(request)
    messages.info(request, "Logout successfully")
    return redirect('admin_login')
    

@login_required
def delete_product(request, pk):
    product = get_object_or_404(Item, pk=pk)
    if request.method == 'GET':
        product.delete()
        messages.info(request, "Product deleted successfully")
        return redirect('admin_products')

@login_required
def add_product(request):
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.image = form.cleaned_data['image']
            product.save()
            messages.success(request, "Product added successfully")
            return redirect('admin_products')
        else:
            messages.error(request, "Please enter all or correct info")
            return redirect('admin_products')
    return render(request, 'admin/products.html')


@login_required
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Catogery added successfully")
            return redirect('admin_products')
        else:
            messages.error(request, "Bad Data or Already Exit")
            return redirect('admin_products')
    return render(request, 'admin/products.html')