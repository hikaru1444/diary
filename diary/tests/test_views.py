from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse

from diary.views import *

UserModel = get_user_model()
env = environ.Env()


class AllViewTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = UserModel.objects.create_user(
            username="admin3", password="password")
        self.data = {'year': 2022, 'month': '1月30日', 'number': 600,
                     'type': '法人', 'manager': 'admin', 'tax_agency': '熊本西',
                     'date': datetime.date.today()}

    def test_main_login_200(self):
        request = self.factory.get(reverse("main"))
        request.user = self.user
        response = views_main(request)
        self.assertEqual(response.status_code, 200)

    def test_main_login_302(self):
        request = self.factory.get(reverse("main"))
        request.user = AnonymousUser()
        response = views_main(request)
        self.assertEqual(response.status_code, 302)

    def test_work_login_200(self):
        request = self.factory.get(reverse("work"))
        request.user = self.user
        response = views_work(request)
        self.assertEqual(response.status_code, 200)

    def test_work_login_302(self):
        request = self.factory.get(reverse("work"))
        request.user = AnonymousUser()
        response = views_work(request)
        self.assertEqual(response.status_code, 302)

    def test_work_btn_r(self):
        request = self.factory.post(reverse("work"), data={
            'btn-r': '',
            'year': 2022,
            'month': 1
        })
        request.user = self.user
        response = views_work(request)
        self.assertEqual(response.status_code, 200)

    def test_work_btn_check(self):
        request = self.factory.post(reverse("work"), data={
            'btn-check': '',
            'year': 2022,
            'month': 1
        })
        request.user = self.user
        response = views_work(request)
        self.assertEqual(response.status_code, 200)

    def test_work_btn_c(self):
        request = self.factory.post(reverse("work"), data={
            'btn-c': '',
            'year': 2022,
            'month': 1,
            'day' : 1,
            'in_time': '9:00',
            'out_time': '18:00',
            'rest_time': '1:00',
            'note': 'test',
            'distance': 1.1,
        })
        request.user = self.user
        response = views_work(request)
        self.assertEqual(response.status_code, 200)

    def test_work_btn_d(self):
        request = self.factory.post(reverse("work"), data={
            'btn-d': '',
            'year': 2022,
            'month': 1,
            'day' : 1,
            'in_time': '9:00',
            'out_time': '18:00',
            'rest_time': '1:00',
            'note': 'test',
            'distance': 1.1,
        })
        request.user = self.user
        response = views_work(request)
        self.assertEqual(response.status_code, 200)

    def test_work_btn_r2(self):
        request = self.factory.post(reverse("work"), data={
            'btn-r2': '',
            'year': 2022,
            'month': 1,
        })
        request.user = self.user
        response = views_work(request)
        self.assertEqual(response.status_code, 200)

    def test_year_adjustment_get(self):
        request = self.client.get(reverse("year_adjustment"), data={})
        self.assertEqual(request.status_code, 200)

    def test_year_adjustment_btn_c(self):
        request = self.client.post(reverse("year_adjustment"), data={
            'btn-c': '',
            'year': self.data['year'],
            'number': self.data['number'],
            'number_choice': self.data['number'],
            'manager': self.data['manager'],
            'tax_agency': self.data['tax_agency'],
        })
        self.assertEqual(request.status_code, 200)

    def test_year_adjustment_btn_r(self):
        request = self.client.post(reverse("year_adjustment"), data={
            'btn-r': '',
            'year': self.data['year'],
            'manager': self.data['manager'],
            'tax_agency': self.data['tax_agency'],
        })
        self.assertEqual(request.status_code, 200)

    def test_year_adjustment_btn_u(self):
        request = self.client.post(reverse("year_adjustment"), data={
            'btn-u': '',
            'year': self.data['year'],
            'number': self.data['number'],
            'tax_agency': '',
            'manager': 'admin',
            'year_adjustment_day': '',
            'personnel': 0,
            'city_paper': 0,
            'city_electronic': 0,
            'star': '',
            'payment_create_date': '',
            'date': '',
            'payment_slip_delivery': '',
            'payment_slip_mail': '',
            'billing_amount': 100,
            'withholding_tax': 100,
            'invoice_number': '',
            'report_create_date': '',
            'filing_date': '',
            'electronic_or_paper': '',
            'billing_amount2': 0,
            'withholding_tax2': 0,
            'note': '',
        })
        self.assertEqual(request.status_code, 200)

    def test_year_adjustment_btn_d(self):
        request = self.client.post(reverse("year_adjustment"), data={
            'btn-d': '',
            'year': self.data['year'],
            'number': self.data['number'],
            'manager': self.data['manager'],
            'tax_agency': self.data['tax_agency'],
        })
        self.assertEqual(request.status_code, 200)

    def test_year_adjustment_btn_p(self):
        request = self.client.post(reverse("year_adjustment"), data={
            'btn-p': '',
            'year': self.data['year'],
            'manager': self.data['manager'],
            'tax_agency': self.data['tax_agency'],
        })
        self.assertEqual(request.status_code, 200)

    def test_filing_get(self):
        request = self.client.get(reverse("filing"), data={})
        self.assertEqual(request.status_code, 200)

    def test_filing_btn_r(self):
        request = self.client.post(reverse("filing"), data={
            'btn-r': '',
            'year': self.data['year'],
            'month': self.data['month'],
        })
        self.assertEqual(request.status_code, 200)

    def test_filing_btn_u(self):
        request = self.client.post(reverse("filing"), data={
            'btn-u': '',
            'year': self.data['year'],
            'month': self.data['month'],
            'number': self.data['number'],
            'tax_agency': self.data['tax_agency'],
            'regional_tax_office': '熊本県税事務所',
            'government_office': '熊本市役所',
            'accounting_date': '1月31日',
            'consumption_tax_category': '一 般',
            'consumption_tax_times': '11回',
            'report_schedule': '有',
            'document1': '確定申告',
            'document2': '相続税',
            'tax_agency_note': '法人税「有」',
            'regional_tax_office_note': '熊本県のみ有り',
            'government_office_note': '無・電子',
            'report_schedule_note': '',
            'consumption_tax_times_note': '',
            'insert_date': self.data['date'],
            'insert_data_note': '',

        })
        self.assertEqual(request.status_code, 200)

    def test_filing_btn_c(self):
        request = self.client.post(reverse("filing"), data={
            'btn-c': '',
            'year': self.data['year'],
            'month': self.data['month'],
            'number': self.data['number'],
            'number_choice': self.data['number'],
        })
        self.assertEqual(request.status_code, 200)

    def test_filing_btn_d(self):
        request = self.client.post(reverse("filing"), data={
            'btn-d': '',
            'year': self.data['year'],
            'month': self.data['month'],
            'number': self.data['number'],
        })
        self.assertEqual(request.status_code, 200)

    def test_filing_btn_p(self):
        request = self.client.post(reverse("filing"), data={
            'btn-p': '',
            'year': self.data['year'],
            'month': self.data['month'],
        })
        self.assertEqual(request.status_code, 200)

    def test_gift_tax_check_get(self):
        request = self.client.get(reverse("gift_tax_check"), data={})
        self.assertEqual(request.status_code, 200)

    def test_gift_tax_check_btn_c(self):
        request = self.client.post(reverse("gift_tax_check"), data={
            'btn-c': '',
            'year': self.data['year'],
            'number': self.data['number'],
            'number_choice': self.data['number'],
        })
        self.assertEqual(request.status_code, 200)

    def test_gift_tax_check_btn_r(self):
        request = self.client.post(reverse("gift_tax_check"), data={
            'btn-r': '',
            'year': self.data['year'],
        })
        self.assertEqual(request.status_code, 200)

    def test_gift_tax_check_btn_u(self):
        request = self.client.post(reverse("gift_tax_check"), data={
            'btn-u': '',
            'year': self.data['year'],
            'number': self.data['number'],
            'tax_agency': self.data['tax_agency'],
            'return_date': '11/11',
            'end_date': '11/11',
            'payment_slip_exist': '有',
            'payment_slip_date': '11/11',
            'report_create_date': '11/11',
            'fair_copy_date ': '11/11',
            'boss_stamp_date': '11/11',
            'client_stamp_date': '11/11',
            'filing_date': '11/11',
            'electronic_or_paper': '紙',
            'reward_billing_amount': 10000,
            'reward_withholding': 10000,
            'copy1': '○',
            'note': '',
        })
        self.assertEqual(request.status_code, 200)

    def test_gift_tax_check_btn_d(self):
        request = self.client.post(reverse("gift_tax_check"), data={
            'btn-d': '',
            'year': self.data['year'],
            'number': self.data['number'],
        })
        self.assertEqual(request.status_code, 200)

    def test_gift_tax_check_btn_p(self):
        request = self.client.post(reverse("gift_tax_check"), data={
            'btn-p': '',
            'year': self.data['year'],
        })
        self.assertEqual(request.status_code, 200)

    def test_withholding_get(self):
        request = self.client.get(reverse("withholding"), data={})
        self.assertEqual(request.status_code, 200)

    def test_withholding_btn_c(self):
        request = self.client.post(reverse("withholding"), data={
            'btn-c': '',
            'year': self.data['year'],
            'tax_agency': self.data['tax_agency'],
            'type': self.data['type'],
            'number': self.data['number'],
            'number_choice': self.data['number'],
        })
        self.assertEqual(request.status_code, 200)

    def test_withholding_btn_r(self):
        request = self.client.post(reverse("withholding"), data={
            'btn-r': '',
            'year': self.data['year'],
            'tax_agency': self.data['tax_agency'],
            'type': self.data['type'],
        })
        self.assertEqual(request.status_code, 200)

    def test_withholding_btn_u(self):
        request = self.client.post(reverse("withholding"), data={
            'btn-u': '',
            'year': self.data['year'],
            'number': self.data['number'],
            'number_choice': self.data['number'],
            'tax_agency': self.data['tax_agency'],
            'type': self.data['type'],
            'withholding_tax_method': '',
            'delivery_date': self.data['date'],
            'mail_date': '',
            'note': ''
        })
        self.assertEqual(request.status_code, 200)

    def test_withholding_btn_d(self):
        request = self.client.post(reverse("withholding"), data={
            'btn-d': '',
            'year': self.data['year'],
            'tax_agency': self.data['tax_agency'],
            'type': self.data['type'],
            'number': self.data['number'],
            'number_choice': self.data['number'],
        })
        self.assertEqual(request.status_code, 200)

    def test_withholding_btn_p(self):
        request = self.client.post(reverse("withholding"), data={
            'btn-p': '',
            'year': self.data['year'],
            'tax_agency': self.data['tax_agency'],
            'type': self.data['type'],
        })
        self.assertEqual(request.status_code, 200)


class LoginTests(TestCase):

    def test_login(self):
        users = UserModel.objects.all()
        for user in users:
            user_login = self.client.login(username=user.username, password=env('USER_PASSWORD'))
            if user_login:
                self.assertEqual(user_login, True)
            else:
                print(user_login.username, "がログインできません。")
                self.assertEqual(user_login, True)
