from django.test import TestCase
from diary.models import *
import datetime


class ModelTests(TestCase):
    def test_menu_other_prefectures(self):
        self.assertEqual(ClientList.objects.filter(prefecture='その他').count(), 0)
    def test_menu_other_accounting_date(self):
        self.assertEqual(ClientList.objects.filter(accounting_date='その他').count(), 0)
    def test_menu_other_tax_agency(self):
        self.assertEqual(ClientList.objects.filter(tax_agency='その他').count(), 0)
    def test_menu_other_regional_tax_office(self):
        self.assertEqual(ClientList.objects.filter(regional_tax_office='その他').count(), 0)
    def test_menu_other_government_office(self):
        self.assertEqual(ClientList.objects.filter(government_office='その他').count(), 0)
    def test_withholding_check(self):
        WithholdingCheck.objects.get_or_create(year=2022, k_number_id=600, defaults={
            'type': "法人", 'tax_agency': "熊本西", 'delivery_date': "11/11", 'mail_date': "11/12",
            'note': "備考", 'withholding_tax_method': "方法"})

    def test_filing_final_tax(self):
        FilingFinalTax.objects.get_or_create(year=2022, k_number_id=600, defaults={
            'report_form_category': "有", 'report_category': "青 色", 'consumption_report': "有", 'filing': "有",
            'sales': "○", 'agriculture': "○", 'real_estate': "○", 'interest': "○", 'dividend': "○",
            'salary': "○", 'pension': "○", 'other': "○", 'comprehensive': "○", 'separation': "○",
            'temporary': "○", 'income_tax': "有り", 'consumption': "有り", 'fair_copy_date': "11/11",
            'seal_check_date': "11/11", 'boss_stamp_date': "11/11", 'electronic_end_date': "11/11",
            'attached_document_filing_date': "11/11",
            'billing_amount': 100, 'withholding': 10, 'note': "備考", 'filing2': "改,行,で,き,る"})

    def test_work(self):
        Work.objects.get_or_create(name_id="admin", date=datetime.date(year=2022, month=7, day=24), defaults={
            'in_time': datetime.time(hour=9, minute=0, second=0),
            'out_time': datetime.time(hour=9, minute=0, second=0),
            'rest_time': datetime.time(hour=9, minute=0, second=0),
            'note': "備考", 'distance': 1.1})

    def test_year_adjustment(self):
        YearAdjustment.objects.get_or_create(k_number_id=600, year=2022, defaults={
            'year_adjustment_day': "11/11", 'personnel': 10, 'city_paper': 10, 'city_electronic': 10,
            'star': "★", 'payment_create_date': "11/11", 'date': "11/11",
            'payment_slip_delivery': "11/11", 'payment_slip_mail': "11/11",
            'billing_amount': 1000, 'withholding_tax': 100, 'invoice_number': "1-1",
            'report_create_date': "11/11", 'filing_date': "11/11", 'electronic_or_paper': "電子",
            'billing_amount2': 100, 'withholding_tax2': 10, 'note': "備考"})

    def test_invoice(self):
        Invoice.objects.get_or_create(k_number_id=600, date=datetime.date(year=2022, month=7, day=24), defaults={
            'reward': "報酬", 'items': "内訳", 'money': 1000, 'consumption': 100,
            'withholding_income_tax': 100, 'reconstruction_tax': 100})

    def test_memo(self):
        Memo.objects.get_or_create(k_number_id=600, defaults={'content_memo': "資料整理内容"})

    def test_filing_form_list(self):
        FilingFormList.objects.get_or_create(year=2022, month="7月31日", k_number_id=600, defaults={
            'accounting_date': "7月31日", 'consumption_tax_category': "有", 'consumption_tax_times': "1回",
            'report_schedule': "有", 'document1': "予定申告", 'document2': "予定申告", 'tax_agency_note': "備考",
            'regional_tax_office_note': "備考", 'government_office_note': "備考", 'report_schedule_note': "備考",
            'insert_date': datetime.date(year=2022, month=7, day=24), 'insert_date_note': "備考"})

    def test_sales_management(self):
        SalesManagement.objects.get_or_create(k_number_id=600, year=2022, defaults={
            'm1': 1000, 'm2': 1000, 'm3': 1000, 'm4': 1000, 'm5': 1000, 'm6': 1000,
            'm7': 1000, 'm8': 1000, 'm9': 1000, 'm10': 1000, 'm11': 1000, 'm12': 1000,
            'first_term': 1000, 'current_term': 1000})

    def test_officer_change(self):
        OfficerChange.objects.get_or_create(k_number_id=600, year=2022, defaults={'note': "備考"})

    def test_gift_tax_(self):
        GiftTax.objects.get_or_create(year=2022, k_number_id=600, defaults={
            'return_date': "11/11", 'end_date': "11/11", 'payment_slip_exist': "有", 'payment_slip_date': "11/11",
            'report_create_date': "11/11", 'fair_copy_date': "11/11", 'boss_stamp_date': "11/11",
            'client_stamp_date': "11/11", 'filing_date': "11/11", 'electronic_or_paper': "電子",
            'reward_withholding': 100, 'reward_billing_amount': 1000, 'copy1': "有", 'note': "備考"})

    def test_schedule_box(self):
        ScheduleBox.objects.get_or_create(k_number_id=600, date=datetime.date(year=2022, month=7, day=24), defaults={
            'filing_type': "電子", 'content': "内容", 'note': "備考"})

    def test_direct_payment(self):
        DirectPayment.objects.get_or_create(year=2022, k_number_id=600, tax_type="源泉税", defaults={
            'm1': "1", 'm2': "1", 'm3': "1", 'm4': "1", 'm5': "1", 'm6': "1", 'm7': "1",
            'm8': "1", 'm9': "1", 'm10': "1", 'm11': "1", 'm12': "1"})
        test = DirectPayment.objects.all()
        self.assertEqual(test[0].k_number_id, 600)
        self.assertEqual(test[0].year, 2022)