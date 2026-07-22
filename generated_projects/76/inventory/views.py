from django.shortcuts import render, redirect
from .models import Product, Sale

def home(request):
    products = Product.objects.all().order_by('-id')
    return render(request, 'list.html', {'objects': products})

def dashboard(request):
    total_products = Product.objects.count()
    total_stock = sum(product.quantity for product in Product.objects.all())
    total_sales = Sale.objects.count()
    return render(request, 'dashboard.html', {'total_products': total_products, 'total_stock': total_stock, 'total_sales': total_sales})

def product_create(request):
    if request.method == 'POST':
        name = request.POST['name']
        category = request.POST['category']
        price = request.POST['price']
        quantity = request.POST['quantity']
        image = request.FILES['image']
        Product.objects.create(name=name, category=category, price=price, quantity=quantity, image=image)
        return redirect('inventory:home')
    return render(request, 'form.html')