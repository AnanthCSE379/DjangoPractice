from django.db import models

# The five complexes used in this lab example.
APARTMENT_NAMES = [
    ('Aster', 'Aster'), ('Birch', 'Birch'), ('Cedar', 'Cedar'),
    ('Daisy', 'Daisy'), ('Elm', 'Elm'),
]

# Your original Student exercise.
class Student(models.Model):
    name = models.CharField(max_length=30)
    age = models.IntegerField()
    marks = models.IntegerField()
    total = models.IntegerField()


# One row describes ONE floor in an apartment complex (5 complexes × 3 floors).
class Apartment(models.Model):
    apartment_name = models.CharField(max_length=100, choices=APARTMENT_NAMES)
    address = models.CharField(max_length=200)
    floor_number = models.IntegerField(choices=[(0, 'Ground'), (1, 'First'), (2, 'Second')])
    total_flats = models.PositiveIntegerField()
    available_flats = models.PositiveIntegerField()
    price_per_sqft = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        # Do not enter the same complex and floor twice.
        unique_together = ['apartment_name', 'floor_number']

    def __str__(self):
        return self.apartment_name


class Registration(models.Model):
    customer_name = models.CharField(max_length=100)
    # A phone number is text: it may start with zero.
    mobile_number = models.CharField(max_length=10)
    email = models.EmailField()
    apartment_name = models.CharField(max_length=100, choices=APARTMENT_NAMES)
    flat_type = models.CharField(
        max_length=5, choices=[('1 BHK', '1 BHK'), ('2 BHK', '2 BHK'), ('3 BHK', '3 BHK')]
    )
    # Keep the original booking price for receipts, even if inventory prices change.
    total_cost = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    def __str__(self):
        return self.customer_name
