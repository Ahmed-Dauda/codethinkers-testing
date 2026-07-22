from django.test import TestCase
from .models import Product, Category, Supplier, Stock, Sale

class InventoryTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics')
        self.supplier = Supplier.objects.create(name='Supplier A', contact_info='Contact Info')
        self.product = Product.objects.create(name='Laptop', price=999.99, category=self.category, supplier=self.supplier)
        self.stock = Stock.objects.create(product=self.product, quantity=10)

    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Laptop')
        self.assertEqual(self.product.price, 999.99)

    def test_stock_management(self):
        self.assertEqual(self.stock.quantity, 10)
