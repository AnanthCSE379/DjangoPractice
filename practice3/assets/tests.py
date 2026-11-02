from django.test import TestCase,Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Asset


class AssetTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user(username='staff',is_staff=True)
        self.client.force_login(self.staff)
        self.data = {'asset_id':'LAB001','name':'Microscope','category':'Instrument',
                     'purchase_date':'2026-11-01','cost':'1500.50',
                     'status':'Active','location':'Lab A'}

    def create_asset(self):
        self.client.post(reverse('assets:add'),self.data)
        return Asset.objects.get(asset_id='LAB001')

    def test_exact_urls(self):
        self.assertEqual(reverse('assets:list'),'/assets/')
        self.assertEqual(reverse('assets:add'),'/assets/add/')
        self.assertEqual(reverse('assets:delete',args=[1]),'/assets/1/delete/')

    def test_staff_required(self):
        asset = self.create_asset()
        self.client.logout()
        for url in ['/assets/','/assets/add/',reverse('assets:delete',args=[asset.id])]:
            self.assertRedirects(self.client.get(url),reverse('admin:login'))
        user = User.objects.create_user(username='student')
        self.client.force_login(user)
        response = self.client.post(reverse('assets:delete',args=[asset.id]))
        self.assertRedirects(response,reverse('admin:login'))
        self.assertEqual(Asset.objects.count(),1)

    def test_add_saves_and_displays_success_message(self):
        response = self.client.post(reverse('assets:add'),self.data,follow=True)
        self.assertRedirects(response,reverse('assets:list'))
        self.assertContains(response,'Asset added successfully')
        self.assertContains(response,'Microscope')
        self.assertIsNotNone(Asset.objects.get().created_at)

    def test_invalid_form_does_not_save(self):
        for changes in [{'cost':'-1'},{'name':''},{'purchase_date':'bad date'}]:
            response = self.client.post(reverse('assets:add'),{**self.data,**changes})
            self.assertEqual(response.status_code,200)
            self.assertTrue(response.context['form'].errors)
        self.assertEqual(Asset.objects.count(),0)

    def test_duplicate_id_shows_field_error(self):
        self.create_asset()
        response = self.client.post(reverse('assets:add'),self.data)
        self.assertIn('asset_id',response.context['form'].errors)
        self.assertEqual(Asset.objects.count(),1)

    def test_newest_first(self):
        first = self.create_asset()
        self.client.post(reverse('assets:add'),{**self.data,'asset_id':'LAB002'})
        response = self.client.get(reverse('assets:list'))
        self.assertEqual(list(response.context['details'].values_list('asset_id',flat=True)),
                         ['LAB002',first.asset_id])

    def test_confirmation_does_not_delete_but_post_does(self):
        asset = self.create_asset()
        url = reverse('assets:delete',args=[asset.id])
        response = self.client.get(url)
        self.assertContains(response,'LAB001 - Microscope')
        self.assertEqual(Asset.objects.count(),1)
        response = self.client.post(url,follow=True)
        self.assertContains(response,'Asset deleted successfully')
        self.assertEqual(Asset.objects.count(),0)
        self.assertEqual(self.client.get(url).status_code,404)

    def test_csrf_required_for_post(self):
        asset = self.create_asset()
        browser = Client(enforce_csrf_checks=True)
        browser.force_login(self.staff)
        url = reverse('assets:delete',args=[asset.id])
        self.assertEqual(browser.post(url).status_code,403)
        browser.get(url)
        token = browser.cookies['csrftoken'].value
        self.assertRedirects(browser.post(url,{'csrfmiddlewaretoken':token}),
                             reverse('assets:list'))
