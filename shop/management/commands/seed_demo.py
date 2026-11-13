import os
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from shop.models import Customer, Product, Sale, TankLevel


class Command(BaseCommand):
    help = "Create demo users and sample data (safe to run on every deploy)"

    def handle(self, *args, **options):
        # Demo user: regular account, NOT staff or superuser
        if not User.objects.filter(username='demo').exists():
            User.objects.create_user('demo', 'demo@example.com', 'WaterDemo2026')

        # Your admin account, password comes from the ADMIN_PASSWORD env variable
        admin_password = os.environ.get('ADMIN_PASSWORD')
        if admin_password and not User.objects.filter(username='andiego_').exists():
            User.objects.create_superuser('andiego_', 'andie.andiego@gmail.com', admin_password)

        # Only seed data into an empty database
        if Customer.objects.exists():
            self.stdout.write("Data already present, skipping.")
            return

        products = {
            size: Product.objects.create(size=size, price=price, stock_quantity=stock)
            for size, price, stock in [
                ('1L', Decimal('10.00'), 100),
                ('5L', Decimal('75.00'), 50),
                ('10L', Decimal('100.00'), 30),
                ('20L', Decimal('150.00'), 25),
            ]
        }

        customers = [
            Customer.objects.create(name='Jane Wanjiru', phone_number='+254712345678',
                                    location='Westlands', discount_percentage=Decimal('5.00')),
            Customer.objects.create(name='Peter Otieno', phone_number='+254723456789',
                                    location='Karen', is_credit_customer=True),
            Customer.objects.create(name='Grace Muthoni', phone_number='+254734567890',
                                    location='Kilimani'),
            Customer.objects.create(name='Samuel Kiptoo', phone_number='+254745678901',
                                    location='Ngong', is_credit_customer=True),
        ]

        # (customer index, size, quantity, paid?, days ago)
        sales = [
            (0, '20L', 2, True, 1), (0, '5L', 3, True, 5), (0, '1L', 10, True, 9),
            (0, '20L', 1, True, 14), (1, '20L', 2, False, 2), (2, '10L', 5, True, 20),
            (3, '5L', 4, False, 3),
        ]
        for idx, size, qty, paid, days_ago in sales:
            customer, product = customers[idx], products[size]
            base = qty * product.price
            discount_rate = Decimal(str(customer.discount_percentage)) / Decimal("100")

            total = base - (base * discount_rate)
            sale = Sale.objects.create(customer=customer, product=product, quantity=qty,
                                       total_amount=total, is_paid=paid)
            # `date` is auto_now_add, so backdate it with update()
            Sale.objects.filter(pk=sale.pk).update(
                date=timezone.now() - timedelta(days=days_ago))

        TankLevel.objects.create(level_percentage=Decimal('65.00'), source='manual')
        self.stdout.write(self.style.SUCCESS("Demo data created."))