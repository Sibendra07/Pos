from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from inventory.models import Category, Products
from pos.models import Sales, salesItems
from purchase.models import PurchaseProduct, Supplier


class Command(BaseCommand):
    help = "Create sample users, inventory, purchases, and sales."

    @transaction.atomic
    def handle(self, *args, **options):
        User = get_user_model()
        admin, created = User.objects.get_or_create(
            username="sales",
            defaults={
                "email": "demo@example.com",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        if created:
            admin.set_password("SalesPass123!")
            admin.save(update_fields=["password"])

        category_data = [
            ("Beverages", "Drinks and refreshments"),
            ("Snacks", "Packaged snacks and quick bites"),
            ("Groceries", "Everyday grocery products"),
            ("Personal Care", "Personal hygiene products"),
            ("Dairy", "Milk, cheese, and dairy products"),
            ("Bakery", "Bread, biscuits, and baked goods"),
            ("Frozen Foods", "Frozen and ready-to-cook items"),
            ("Household", "Cleaning and household supplies"),
            ("Stationery", "Office and school supplies"),
            ("Electronics", "Small electronics and accessories"),
        ]
        categories = {
            name: Category.objects.get_or_create(
                name=name, defaults={"description": description}
            )[0]
            for name, description in category_data
        }

        supplier_data = [
            ("Everest Wholesale", "01-5550101 | sales@everest.example"),
            ("Kathmandu Distributors", "01-5550102 | orders@kathmandu.example"),
            ("Himalayan Traders", "01-5550103 | hello@himalayan.example"),
            ("Pokhara Supply Co.", "061-5550104 | contact@pokharasupply.example"),
            ("Annapurna Imports", "01-5550105 | info@annapurnaimports.example"),
            ("Sagarmatha Foods", "01-5550106 | sales@sagarmathafoods.example"),
            ("Lumbini General Traders", "071-5550107 | orders@lumbinitraders.example"),
        ]
        suppliers = [
            Supplier.objects.get_or_create(
                name=name, defaults={"contact_info": contact}
            )[0]
            for name, contact in supplier_data
        ]

        product_data = [
            # Beverages
            ("BEV-001", "Mineral Water 1L", "Beverages", "20.00", "12.00"),
            ("BEV-002", "Cola 500ml", "Beverages", "60.00", "38.00"),
            ("BEV-003", "Orange Juice 1L", "Beverages", "180.00", "125.00"),
            ("BEV-004", "Lemon Iced Tea 500ml", "Beverages", "70.00", "45.00"),
            ("BEV-005", "Energy Drink 250ml", "Beverages", "150.00", "100.00"),
            ("BEV-006", "Instant Coffee 100g", "Beverages", "320.00", "240.00"),
            # Snacks
            ("SNK-001", "Potato Chips", "Snacks", "80.00", "50.00"),
            ("SNK-002", "Chocolate Bar", "Snacks", "100.00", "65.00"),
            ("SNK-003", "Salted Peanuts", "Snacks", "90.00", "55.00"),
            ("SNK-004", "Popcorn 100g", "Snacks", "60.00", "35.00"),
            ("SNK-005", "Cheese Crackers", "Snacks", "95.00", "60.00"),
            # Groceries
            ("GRO-001", "Basmati Rice 5kg", "Groceries", "850.00", "700.00"),
            ("GRO-002", "Cooking Oil 1L", "Groceries", "240.00", "195.00"),
            ("GRO-003", "Sugar 1kg", "Groceries", "110.00", "85.00"),
            ("GRO-004", "Black Tea 250g", "Groceries", "220.00", "160.00"),
            ("GRO-005", "Lentils (Dal) 1kg", "Groceries", "190.00", "150.00"),
            ("GRO-006", "Salt 1kg", "Groceries", "35.00", "22.00"),
            ("GRO-007", "Wheat Flour 2kg", "Groceries", "150.00", "110.00"),
            # Personal Care
            ("CAR-001", "Bath Soap", "Personal Care", "75.00", "45.00"),
            ("CAR-002", "Toothpaste 100g", "Personal Care", "145.00", "95.00"),
            ("CAR-003", "Shampoo 200ml", "Personal Care", "260.00", "190.00"),
            ("CAR-004", "Hand Sanitizer 100ml", "Personal Care", "120.00", "80.00"),
            # Dairy
            ("DRY-001", "Fresh Milk 1L", "Dairy", "95.00", "70.00"),
            ("DRY-002", "Cheese Slices 200g", "Dairy", "280.00", "210.00"),
            ("DRY-003", "Butter 250g", "Dairy", "310.00", "240.00"),
            ("DRY-004", "Yogurt 400g", "Dairy", "130.00", "90.00"),
            # Bakery
            ("BAK-001", "White Bread Loaf", "Bakery", "65.00", "40.00"),
            ("BAK-002", "Digestive Biscuits", "Bakery", "85.00", "55.00"),
            ("BAK-003", "Cupcakes (Pack of 4)", "Bakery", "180.00", "120.00"),
            # Frozen Foods
            ("FRZ-001", "Frozen Peas 500g", "Frozen Foods", "160.00", "115.00"),
            ("FRZ-002", "Chicken Nuggets 400g", "Frozen Foods", "420.00", "320.00"),
            ("FRZ-003", "Ice Cream Tub 500ml", "Frozen Foods", "350.00", "260.00"),
            # Household
            ("HSE-001", "Dish Washing Liquid 500ml", "Household", "140.00", "95.00"),
            ("HSE-002", "Laundry Detergent 1kg", "Household", "260.00", "195.00"),
            ("HSE-003", "Trash Bags (Pack of 20)", "Household", "110.00", "75.00"),
            # Stationery
            ("STA-001", "Ballpoint Pen (Pack of 5)", "Stationery", "50.00", "30.00"),
            ("STA-002", "A4 Notebook", "Stationery", "70.00", "45.00"),
            ("STA-003", "Sticky Notes Pack", "Stationery", "90.00", "60.00"),
            # Electronics
            ("ELC-001", "USB Cable Type-C", "Electronics", "250.00", "170.00"),
            ("ELC-002", "Wired Earphones", "Electronics", "450.00", "320.00"),
            ("ELC-003", "AA Batteries (Pack of 4)", "Electronics", "180.00", "120.00"),
        ]

        products = []
        for index, (code, name, category_name, price, cost) in enumerate(product_data):
            product, _ = Products.objects.get_or_create(
                code=code,
                defaults={
                    "name": name,
                    "description": "Sample product for demonstration",
                    "category": categories[category_name],
                    "price": Decimal(price),
                    "cost": Decimal("0"),
                    "quantity": 0,
                },
            )
            purchase, purchase_created = PurchaseProduct.objects.get_or_create(
                supplier=suppliers[index % len(suppliers)],
                product=product,
                defaults={
                    "cost": Decimal(cost),
                    "qty": Decimal(40 + (index % 4) * 10),
                },
            )
            if not purchase_created and product.cost <= 0:
                purchase.cost = Decimal(cost)
                purchase.qty = Decimal(40 + (index % 4) * 10)
                purchase.save()
            products.append(product)

        num_products = len(products)

        # Build a larger, varied set of sales baskets (mod against num_products
        # so this stays safe even if the product list above is trimmed further).
        raw_baskets = [
            (0, 3), (1, 6), (4, 8), (7, 10), (2, 9),
            (11, 14, 20), (5, 17), (12, 22, 30), (3, 25),
            (18, 27, 33), (9, 15), (21, 28), (6, 19, 36),
            (13, 24), (2, 31, 38), (16, 26), (10, 23, 35),
            (1, 29, 40), (8, 32), (14, 37, 39),
        ]
        product_indexes_list = [
            tuple(i % num_products for i in basket) for basket in raw_baskets
        ]

        customer_names = [
            "Demo Customer", "Sita Sharma", "Ram Thapa", "Anita Gurung",
            "Bikash Rai", "Priya Shrestha", "Suresh Karki", "Maya Tamang",
            "Nabin Adhikari", "Sunita Poudel",
        ]

        sales_created = 0
        for sale_number, product_indexes in enumerate(product_indexes_list, start=1):
            sale, created = Sales.objects.get_or_create(
                code="DEMO-SALE-{0:03d}".format(sale_number),
                defaults={
                    "date_added": timezone.now() - timedelta(
                        days=len(product_indexes_list) - sale_number
                    ),
                    "cliente": "{0} {1}".format(
                        customer_names[sale_number % len(customer_names)],
                        sale_number,
                    ),
                },
            )
            if not created:
                continue

            subtotal = 0.0
            for line_number, product_index in enumerate(product_indexes, start=1):
                product = products[product_index]
                quantity = 1 + (sale_number + line_number) % 3
                price = float(product.price)
                total = price * quantity
                salesItems.objects.create(
                    sale=sale,
                    product=product,
                    price=price,
                    qty=quantity,
                    total=total,
                )
                subtotal += total
            sale.sub_total = subtotal
            sale.grand_total = subtotal
            sale.tendered_amount = subtotal + 100
            sale.amount_change = 100
            sale.save(update_fields=[
                "sub_total", "grand_total", "tendered_amount", "amount_change"
            ])
            sales_created += 1

        self.stdout.write(self.style.SUCCESS("Demo data is ready."))
        self.stdout.write(
            "Admin login: sales / SalesPass123! | "
            "Categories: {0} | Products: {1} | Suppliers: {2} | "
            "Purchases: {3} | New sales: {4}".format(
                Category.objects.count(),
                Products.objects.count(),
                Supplier.objects.count(),
                PurchaseProduct.objects.count(),
                sales_created,
            )
        )