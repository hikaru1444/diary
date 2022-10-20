from django.test import TestCase
from diary.forms import *
from diary import forms_choices as f
import datetime
from diary.views import defs


# FormTest
class AllFormTests(TestCase):

    def test_year_form(self):
        params = {'year': 2022}
        form = YearForm(params)
        self.assertTrue(form.is_valid())

    def test_year_month_form(self):
        params = {'year': 2022, 'month': '1月31日'}
        form = YearMonthForm(params)
        self.assertTrue(form.is_valid())

    def test_year_month_number_form(self):
        params = {'year': 2022, 'month': '1月31日', 'number': 600, 'number_choice': ''}
        form = YearMonthNumberForm(params)
        self.assertTrue(form.is_valid())

    def test_year_manager_tax_agency_form(self):
        params = {'year': 2022, 'manager': 'admin', 'tax_agency': '熊本西'}
        form = YearManageTaxAgencyForm(params)
        self.assertTrue(form.is_valid())

    def test_year_tax_agency_type_form(self):
        params = {'year': 2022, 'tax_agency': '熊本西', 'type': '法人'}
        form = YearTaxAgencyTypeForm(params)
        self.assertTrue(form.is_valid())

    def test_year_number_form(self):
        params = {'year': 2022, 'number': 600, 'number_choice': ''}
        form = YearNumberForm(params)
        self.assertTrue(form.is_valid())

        params = {'year': 2022, 'number': 600, 'number_choice': 600}
        form = YearNumberForm(params)
        form.fields['number_choice'].choices = defs.number_choice()
        self.assertTrue(form.is_valid())

    def test_schedule_box(self):
        params = {'number': 600, 'date': datetime.date.today(), 'filing_type': '予定',
                  'content': '内容', 'note': '備考'}
        form = ScheduleBoxForm(params)
        self.assertTrue(form.is_valid())

    def test_direct_payment_form(self):
        params = {'year': 2022, 'number': 600, 'tax_type': '源泉税', 'm1': '1/1', 'm2': '2/1',
                  'm3': '3/1', 'm4': '4/1', 'm5': '5/1', 'm6': '6/1', 'm7': '7/1', 'm8': '8/1',
                  'm9': '9/1', 'm10': '10/1', 'm11': '11/1', 'm12': '12/1', }
        form = DirectPaymentForm(params)
        self.assertTrue(form.is_valid())

    def test_filing_form(self):
        params = {'year': 2022, 'month': '1月31日', 'number': 600, 'accounting_date': '1月31日',
                  'consumption_tax_category': '一般', 'consumption_tax_times': '1回', 'report_schedule': '有',
                  'document1': '確定申告', 'document2': '法人税,消費税申告', 'tax_agency_note': '法人税「有」',
                  'regional_tax_office_note': '有', 'city_note': '有', 'report_schedule_note': 'a',
                  'insert_date': datetime.datetime.today(), 'insert_date_note': 'a', }
        form = FilingForm(params)
        self.assertTrue(form.is_valid())

    def test_main_form(self):
        params = {'username': f.users[1][0]}
        form = MainForm(params)
        self.assertTrue(form.is_valid())

    def test_main_form2(self):
        params = {'username': 'hikaru'}
        form = MainForm(params)
        self.assertFalse(form.is_valid())

    def test_withholding_form(self):
        params = {'year': 2022, 'number': 600, 'tax_agency': '熊本西', 'type': '個人',
                  'delivery_date': datetime.date.today(), 'mail_date': datetime.date.today(), 'note': 'a', }
        form = WithholdingForm(params)
        self.assertTrue(form.is_valid())

    def test_sales_management_form(self):
        params = {'year': 2022, 'bank': '熊本ファミリー銀行', 'number': 600, 'month': '1',
                  'money': 10000, 'sales_withhold': '売上', }
        form = SalesManagementForm(params)
        self.assertTrue(form.is_valid())

    def test_filing_final_tax_form(self):
        params = {'manager': f.users[1][1], 'tax_agency': '熊本西', 'number': 100, 'year': 2022,
                  'report_form_category': 'A', 'report_category': '青 色', 'consumption_report': '有',
                  'filing': '有', 'sales': '○', 'agriculture': '○', 'real_estate': '○', 'interest': '○', 'dividend': '○',
                  'salary': '○', 'pension': '○', 'other': '○', 'comprehensive': '○', 'separation': '○',
                  'temporary': '○',
                  'income_tax': '有り', 'consumption': '有り', 'fair_copy_date': '11/11', 'seal_check_date': '11/11',
                  'boss_stamp_date': '11/11', 'electronic_end_date': '11/11', 'attached_document_filing_date': '11/11',
                  'billing_amount': 11, 'withholding': 11, 'note': '-', 'filing2': '-',
                  }
        form = FilingFinalTaxForm(params)
        self.assertTrue(form.is_valid())

    def test_year_adjustment_form(self):
        params = {'number': 100, 'year': 2019, 'year_adjustment_day': '11/11', 'personnel': 1,
                  'city_paper': 1, 'city_electronic': 1, 'star': '★', 'payment_create_date': '1/1',
                  'date': '11/11', 'payment_slip_delivery': '11/11', 'payment_slip_mail': '11/11',
                  'billing_amount': 100, 'withholding_tax': 100, 'invoice_number': '1-48',
                  'report_create_date': '11/11', 'filing_date': '11/11', 'electronic_or_paper': '電子',
                  'billing_amount2': 100, 'withholding_tax2': 100, 'note': '-', 'tax_agency': '熊本西',
                  'type': '個人', }
        form = YearAdjustmentForm(params)
        self.assertTrue(form.is_valid())

    def test_officer_change_form(self):
        params = {'number': 100, 'year': 2019, 'note': 'note'}
        form = OfficerChangeForm(params)
        self.assertTrue(form.is_valid())

    def test_memo_form(self):
        params = {'name': f.manager[1][0], 'number': 100, 'content': 'content'}
        form = MemoForm(params)
        self.assertTrue(form.is_valid())

    def test_gift_tax_form(self):
        params = {'year': 2019, 'number': 100, 'electronic_or_paper': '電子', 'return_date': '1/1',
                  'end_date': '1/1', 'payment_slip_exist': '有', 'payment_slip_date': '1/1',
                  'report_create_date': '1/1',
                  'fair_copy_date': '1/1', 'boss_stamp_date': '1/1', 'client_stamp_date': '1/1',
                  'filing_date': '1/1', 'reward_billing_amount': 1, 'reward_withholding': 1,
                  'copy1': '○', 'note': 'note'}
        form = GiftTaxCheckForm(params)
        self.assertTrue(form.is_valid())

    def test_invoice_form(self):
        params = {'date': '2019-04-11', 'number': 100, 'content': '税務顧問報酬', 'items': '内訳',
                  'money': 100, 'transfer_date': '1月1日'}
        form = InvoiceCreateForm(params)
        self.assertTrue(form.is_valid())

    def test_client_search_form(self):
        params = {'name': '会社'}
        form = ClientSearchForm(params)
        self.assertTrue(form.is_valid())

    def test_involvement_form(self):
        params = {'type': '個人', 'tax_agency': '熊本西', 'date': '2022-01-01'}
        form = InvolvedRosterForm(params)
        self.assertTrue(form.is_valid())

    def test_involvement_form2(self):
        params = {'type': 'あいうえお', 'tax_agency': 'あいうえお', 'date': '2022-01-01'}
        form = InvolvedRosterForm(params)
        self.assertFalse(form.is_valid())

    def test_work_form1(self):
        params = {'name': 'admin', 'year': 2000, 'month': 1, 'day': 30,
                  'in_time': '09:00', 'out_time': '17:00', 'rest_time': '0:00',
                  'note': '-', 'distance': 1}
        form = WorkForm(params)
        self.assertTrue(form.is_valid())

    def test_work_form2(self):
        for i in range(1, len(f.users)):  # ''をテストしないようにするため
            params = {'name': f.users[i][0], 'year': 2000, 'month': 2, 'day': 1,
                      'in_time': '09:00', 'out_time': '17:00', 'rest_time': '1:00', 'note': '-', 'distance': 1}
            form = WorkForm(params)
            self.assertTrue(form.is_valid())

    def test_print_request_form(self):
        params = {'number': 600}
        form = PrintRequestForm(params)
        self.assertTrue(form.is_valid())

    def test_client_detail_form(self):
        params = {
            'type': '法人',
            'k_number': '600',
            'k_ruby': 'usui',
            'k_name': '臼井',
            'company_name': '株式会社臼井',
            'post_number ': '123-4567',
            'prefecture': '熊本県',
            'city': '熊本市',
            'tell_number': '123-4567-8901',
            'fax_number': '12-3456-7890',
            'representative_ruby': 'usui',
            'representative_mei': '臼井',
            'representative_post_numb': '123-4567',
            'representative_address': '熊本',
            'manager1': f.manager[0][0],
            'manager2': f.manager[0][0],
            'manager_check': '有',
            'accounting_date': '1月31日',
            'tax_agency': '熊本西',
            'regional_tax_office': '熊本県税事務所',
            'government_office': '熊本市役所',
            'business_category': '法人',
            'report_category': '青 色',
            'consumption_tax_category': '一 般',
            'withholding_tax_method': '毎月納付',
            'sales_management': '',
            'report_schedule': '有',
            'year_adjustment_check': '有',
            'consumption_tax_times': '1回',
            'depreciable_assets': '有',
            'extended_report': '有',
            'form_of_involvement': 'その他',
            'k_corporate_tax': '○',
            'k_prefecture_tax': '○',
            'k_city': '○',
            'k_consumption': '○',
            'k_income_tax ': '○',
            'report_gift_tax': '○',
            'add_memo': '有',
            'contract_cancellation': '有',
            'involvement_date': '',
            'create_date': datetime.date.today(),
            'last_update': datetime.date.today(),
            't_filing': '',
            't_corporate_registration': '',
            't_important_points': '',
            't_content': '',
            't_start_date': '',
            't_end_date': '',
            't_history': '',
            'content_memo': '',
            'electronic_report': '有',
        }
        form = ClientDetailForm(params)
        self.assertTrue(form.is_valid())
