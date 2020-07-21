from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from django.contrib.auth import login,logout,authenticate
from product.models import Item, Rating, Cart, Order
from product.forms import ItemForm
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

def admin(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request, "admin/dashboard.html")
    else:
        return redirect('admin_login')

def product_list(request):
    object_list = Item.objects.all()
    if 'product' in request.GET:
        product_name = request.GET['product']
        if product_name:
            object_list = Item.objects.filter(title__iexact = product_name)
    return render(request, 'admin/products.html', {'object_list': object_list})


def user_list(request):
    object_list = User.objects.all()
    if 'user' in request.GET:
        username = request.GET['user']
        if username:
            object_list = User.objects.filter(username__iexact = username)
    return render(request, 'admin/users.html', {'object_list': object_list})

class AdminUserView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = 'admin/users.html'

def admin_login(request):
    if request.user.is_superuser:
        return redirect('admin_dashboad')
    else:
        if request.method == 'POST':
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            if user is None:
                return render(request, 'admin/admin_login.html', {'form': AuthenticationForm(), 'error': 'Invalid User'})
            if user.is_superuser:
                login(request, user)
                return redirect('admin_dashboad')
            else:
                return render(request, 'admin/admin_login.html', {'form': AuthenticationForm(), 'error': 'You are not Authorize to access with this account'})
        else:
            return render(request, 'admin/admin_login.html', {'form': AuthenticationForm(),})


@login_required
def product_details(request, pk):
    product = get_object_or_404(Item, pk = pk)
    final_price = product.price - product.discount_price
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            if form.cleaned_data['image']:
                product.image = form.cleaned_data['image']
            else:
                product.image = form.cleaned_data['old_image']
            product.save()
            return render(request, 'admin/product_details.html', {'product': product, 'final_price': final_price})
        else:
            return render(request, '<h2>bad</h2>')
    return render(request, 'admin/product_details.html', {'product': product,'final_price': final_price})


@login_required
def admin_logout(request):
    logout(request)
    return redirect('admin_login')
    

@login_required
def delete_product(request, pk):
    product = get_object_or_404(Item, pk=pk)
    if request.method == 'GET':
        product.delete()
        return redirect('admin_products')

@login_required
def add_product(request):
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.image = form.cleaned_data['image']
            product.save()
            return redirect('admin_products')
        else:
            return render(request, '<h2>bad</h2>')
    return render(request, 'admin/products.html', context)
