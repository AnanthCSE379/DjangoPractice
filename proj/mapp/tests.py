from django.test import TestCase
from django.urls import reverse
from django.core.management import call_command
from .forms import RegistrationForm
from .models import Apartment, Registration


class BuildingTests(TestCase):
    def setUp(self):
        for floor in range(3):
            Apartment.objects.create(
                apartment_name='Aster', address='Park Road', floor_number=floor,
                total_flats=2, available_flats=2, price_per_sqft=5000,
            )
        self.data = {
            'customer_name': 'Ananth', 'mobile_number': '0123456789',
            'email': 'ananth@example.com', 'apartment_name': 'Aster', 'flat_type': '3 BHK',
        }

    def availability(self, floor):
        return Apartment.objects.get(floor_number=floor).available_flats

    def book(self):
        response = self.client.post(reverse('register_flat'), self.data)
        self.assertEqual(response.status_code, 302)
        return Registration.objects.get()

    def test_required_pages_and_empty_customer_list(self):
        for url in ['/buildingapp/home', '/buildingapp/registerFlat',
                    '/buildingapp/dispApartment', '/buildingapp/dispRegistration']:
            self.assertEqual(self.client.get(url).status_code, 200)
        self.assertContains(self.client.get(reverse('display_registrations')),
                            'No registered customers.')

    def test_create_each_flat_type_and_receipt(self):
        for flat_type, floor, area in [('3 BHK', 0, 1200), ('2 BHK', 1, 1000),
                                       ('1 BHK', 2, 800)]:
            response = self.client.post(reverse('register_flat'),
                                        {**self.data, 'flat_type': flat_type})
            self.assertEqual(response.status_code, 302)
            customer = Registration.objects.latest('id')
            self.assertEqual(customer.total_cost, area * 5000)
            self.assertEqual(self.availability(floor), 1)
            receipt = self.client.get(response.url)
            self.assertContains(receipt, 'Ananth')
            self.assertContains(receipt, f'Area: {area} sq. ft.')

    def test_mobile_validation(self):
        for mobile in ['123', '12345678901', '123456789x', '１２３４５６７８９０']:
            form = RegistrationForm({**self.data, 'mobile_number': mobile})
            self.assertFalse(form.is_valid())
            self.assertIn('mobile_number', form.errors)
        self.assertTrue(RegistrationForm(self.data).is_valid())

    def test_sold_out_and_missing_floor_do_not_create_booking(self):
        Apartment.objects.filter(floor_number=0).update(available_flats=0)
        response = self.client.post(reverse('register_flat'), self.data)
        self.assertContains(response, 'No flats available')
        self.assertEqual(Registration.objects.count(), 0)
        Apartment.objects.filter(floor_number=0).delete()
        response = self.client.post(reverse('register_flat'), self.data)
        self.assertContains(response, 'does not have the requested floor')
        self.assertEqual(Registration.objects.count(), 0)

    def test_update_contact_then_move_flat(self):
        customer = self.book()
        url = reverse('edit_registration', args=[customer.pk])
        self.assertContains(self.client.get(url), 'Ananth')
        response = self.client.post(url, {**self.data, 'customer_name': 'Ravi'})
        self.assertEqual(response.status_code, 302)
        customer.refresh_from_db()
        self.assertEqual(customer.customer_name, 'Ravi')
        self.assertEqual(self.availability(0), 1)
        response = self.client.post(url, {**self.data, 'flat_type': '1 BHK'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.availability(0), 2)
        self.assertEqual(self.availability(2), 1)
        customer.refresh_from_db()
        self.assertEqual(customer.total_cost, 4000000)

    def test_failed_move_keeps_original_booking_and_inventory(self):
        customer = self.book()
        Apartment.objects.filter(floor_number=2).update(available_flats=0)
        response = self.client.post(reverse('edit_registration', args=[customer.pk]),
                                    {**self.data, 'flat_type': '1 BHK'})
        self.assertContains(response, 'No flats available')
        customer.refresh_from_db()
        self.assertEqual(customer.flat_type, '3 BHK')
        self.assertEqual(self.availability(0), 1)

    def test_contact_edit_preserves_original_price(self):
        customer = self.book()
        Apartment.objects.filter(floor_number=0).update(price_per_sqft=7000)
        self.client.post(reverse('edit_registration', args=[customer.pk]),
                         {**self.data, 'customer_name': 'Ravi'})
        customer.refresh_from_db()
        self.assertEqual(customer.total_cost, 6000000)
        self.assertEqual(self.availability(0), 1)

    def test_missing_previous_inventory_prevents_new_allocation(self):
        customer = self.book()
        # Simulate an inventory row being removed manually after registration.
        Apartment.objects.filter(floor_number=0).delete()
        response = self.client.post(reverse('edit_registration', args=[customer.pk]),
                                    {**self.data, 'flat_type': '1 BHK'})
        self.assertContains(response, 'Previous inventory is missing or inconsistent')
        self.assertEqual(self.availability(2), 2)
        customer.refresh_from_db()
        self.assertEqual(customer.flat_type, '3 BHK')

    def test_move_to_another_complex(self):
        customer = self.book()
        other = Apartment.objects.create(
            apartment_name='Birch', address='Lake Road', floor_number=0,
            total_flats=1, available_flats=1, price_per_sqft=4000,
        )
        response = self.client.post(reverse('edit_registration', args=[customer.pk]),
                                    {**self.data, 'apartment_name': 'Birch'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.availability_for_aster(), 2)
        other.refresh_from_db()
        customer.refresh_from_db()
        self.assertEqual(other.available_flats, 0)
        self.assertEqual(customer.total_cost, 4800000)

    def test_delete_restores_inventory_and_requires_post(self):
        customer = self.book()
        url = reverse('delete_registration', args=[customer.pk])
        self.assertEqual(self.client.get(url).status_code, 405)
        self.assertEqual(Registration.objects.count(), 1)
        self.assertRedirects(self.client.post(url), reverse('display_registrations'))
        self.assertEqual(Registration.objects.count(), 0)
        self.assertEqual(self.availability(0), 2)
        self.assertEqual(self.client.get(reverse('receipt', args=[customer.pk])).status_code, 404)

    def test_sample_inventory_is_repeatable(self):
        call_command('seed_apartments', verbosity=0)
        Apartment.objects.filter(apartment_name='Aster', floor_number=0).update(available_flats=1)
        call_command('seed_apartments', verbosity=0)
        self.assertEqual(Apartment.objects.count(), 15)
        self.assertEqual(Apartment.objects.values('apartment_name').distinct().count(), 5)
        self.assertEqual(self.availability_for_aster(), 1)

    def availability_for_aster(self):
        return Apartment.objects.get(apartment_name='Aster', floor_number=0).available_flats
