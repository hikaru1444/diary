from django.test import TestCase, Client
from django.urls import reverse


# UrlsTest
class UrlsTests(TestCase):
    list_return_200 = [
        'client_search',
        'involved_roster',
        'client_input',
        'invoice_create',
        'gift_tax_check',
        'memo',
        'officer_change',
        'filing_final_tax',
        'sales_management',
        'withholding',
        'print_request',
        'document',
        'filing',
        'direct_payment',
        'schedule_box',
        'login',
        'year_adjustment', ]

    list_return_302 = [
        'work',
        'main',
        'client_detail',
    ]

    def test_return_200(self):
        for i in range(len(self.list_return_200)):
            response = Client().get(reverse(self.list_return_200[i]))
            if response.status_code != 200:
                print("error!", self.list_return_200[i])
            self.assertEqual(response.status_code, 200)

    def test_return_302(self):
        for i in range(len(self.list_return_302)):
            response = Client().get(reverse(self.list_return_302[i]))
            if response.status_code != 302:
                print("error!", self.list_return_302[i])
            self.assertEqual(response.status_code, 302)
