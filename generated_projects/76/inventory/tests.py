from django.test import TestCase
from .models import Product, Sale

class ProductModelTest(TestCase):
    def setUp(self):
        Product.objects.create(name='Test Product', category='Test Category', price=10.00, quantity=100)

    def test_product_str(self):
        product = Product.objects.get(name='Test Product')
        self.assertEqual(str(product), 'Test Product')

class SaleModelTest(TestCase):
    def setUp(self):
        product = Product.objects.create(name='Test Product', category='Test Category', price=10.00, quantity=100)
        Sale.objects.create(product=product, quantity_sold=10)

    def test_sale_str(self):
        sale = Sale.objects.get(quantity_sold=10)
        self.assertEqual(str(sale), 'Sale of 10 Test Product')