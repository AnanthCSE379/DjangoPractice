from django.contrib import admin
from mapp.models import Apartment, Student

admin.site.register(Student)


class ApartmentAdmin(admin.ModelAdmin):
    # Apartment inventory can be created, read, updated and deleted in admin.
    list_display = ['id', 'apartment_name', 'address', 'floor_number',
                    'total_flats', 'available_flats', 'price_per_sqft']
    ordering = ['apartment_name', 'floor_number']
    search_fields = ['address']
    list_filter = ['floor_number']


admin.site.register(Apartment, ApartmentAdmin)

