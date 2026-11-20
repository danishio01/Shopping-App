
from decimal import Decimal

from django.core.management.base import BaseCommand

from shop.models import Product


class Command(BaseCommand):

    help = "Add sample products to the database"

    def handle(self, *args, **options):

        products = [
            {
                "name": "Wireless Mouse",
                "description": (
                    "Ergonomic wireless mouse "
                    "with smooth tracking."
                ),
                "price": Decimal("799.00"),
                "stock": 10,
                "is_available": True,
            },
            {
                "name": "Mechanical Keyboard",
                "description": (
                    "RGB mechanical keyboard "
                    "with comfortable typing."
                ),
                "price": Decimal("2499.00"),
                "stock": 8,
                "is_available": True,
            },
            {
                "name": "Bluetooth Headphones",
                "description": (
                    "Wireless headphones with "
                    "excellent sound quality."
                ),
                "price": Decimal("1999.00"),
                "stock": 5,
                "is_available": True,
            },
        ]

        for product_data in products:

            product, created = Product.objects.get_or_create(
                name=product_data["name"],
                defaults=product_data,
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created: {product.name}"
                    )
                )
            else:
                self.stdout.write(
                    f"Already exists: {product.name}"
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Sample products ready!"
            )
        )
