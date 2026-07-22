from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Prefetch
from .models import Product, Category, Supplier, Stock, Sale

class HomeView(ListView):
    template_name = 'home.html'
    context_object_name = 'home'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all().order_by('-id')
        context['categories'] = Category.objects.all().order_by('-id')
        context['suppliers'] = Supplier.objects.all().order_by('-id')
        return context

class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'
    paginate_by = 25

    def get_queryset(self):
        return (
            super().get_queryset()
            .select_related('category', 'supplier')
            .only('id', 'name', 'price', 'category__name', 'supplier__name', 'created_at')
            .order_by('-id')
        )

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'

    def get_queryset(self):
        return (
            super().get_queryset()
            .select_related('category', 'supplier')
            .prefetch_related(
                Prefetch('stock_set', queryset=Stock.objects.select_related('product'))
            )
            .order_by('-id')
        )

class ProductCreateView(CreateView):
    model = Product
    template_name = 'product_form.html'
    fields = '__all__'
    success_url = '/products/'

class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'product_form.html'
    fields = '__all__'
    success_url = '/products/'

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product_confirm_delete.html'
    success_url = '/products/'

class SaleListView(ListView):
    model = Sale
    template_name = 'sale_list.html'
    context_object_name = 'sales'
    paginate_by = 25

    def get_queryset(self):
        return (
            super().get_queryset()
            .select_related('product', 'product__category')
            .order_by('-date')
        )