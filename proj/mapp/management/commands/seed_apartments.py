from django.core.management.base import BaseCommand
from mapp.models import Apartment


class Command(BaseCommand):
    help = 'Add five sample apartment complexes, each with floors 0, 1 and 2.'

    def handle(self, *args, **options):
        # Demo values: the question does not specify names, counts or prices.
        complexes = [
            ('Aster', '10 Park Road', 5000),
            ('Birch', '20 Lake Road', 4500),
            ('Cedar', '30 Main Road', 4000),
            ('Daisy', '40 Garden Road', 5500),
            ('Elm', '50 Hill Road', 6000),
        ]
        added = 0
        for name, address, price in complexes:
            for floor in range(3):
                # Running this twice does NOT reset availability or overwrite existing data.
                _, created = Apartment.objects.get_or_create(
                    apartment_name=name, floor_number=floor,
                    defaults={'address': address, 'total_flats': 5,
                              'available_flats': 5, 'price_per_sqft': price},
                )
                added += created
        self.stdout.write(self.style.SUCCESS(f'Added {added} apartment-floor rows.'))
