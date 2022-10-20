import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.utils import timezone
from diary import forms_choices as f


class ClientList(models.Model):
    type = models.CharField(verbose_name="分類", max_length=10, blank=True, default="",
                            choices=f.type_choices)
    k_number = models.IntegerField(verbose_name="顧問先番号", unique=True)
    k_ruby = models.CharField(verbose_name="フリガナ", max_length=100, blank=True, default="")
    k_name = models.CharField(verbose_name="顧問先名", max_length=100, blank=True, default="")
    company_name = models.CharField(verbose_name="会社名", max_length=100, blank=True, default="")
    post_number = models.CharField(verbose_name="郵便番号", max_length=10, blank=True, default="")
    prefecture = models.CharField(verbose_name="都道府県", max_length=10, blank=True, default="", choices=f.prefecture)
    city = models.CharField(verbose_name="住所", max_length=100, blank=True, default="")
    tell_number = models.CharField(verbose_name="電話番号", max_length=13, blank=True, default="")
    fax_number = models.CharField(verbose_name="FAX番号", max_length=20, blank=True, default="")
    representative_ruby = models.CharField(verbose_name="フリガナ", max_length=100, blank=True, default="")
    representative_mei = models.CharField(verbose_name="代表者名", max_length=100, blank=True, default="")
    representative_post_number = models.CharField(verbose_name="代表者郵便番号", max_length=10, blank=True, default="")
    representative_address = models.CharField(verbose_name="代表者住所", max_length=100, blank=True, default="")
    manager1 = models.CharField(verbose_name="担当1", max_length=100, blank=True, default="", choices=f.manager)
    manager2 = models.CharField(verbose_name="担当2", max_length=100, blank=True, default="", choices=f.manager)
    manager_check = models.CharField(verbose_name="担当者チェック", max_length=1, blank=True, default="", choices=f.check)
    accounting_date = models.CharField(verbose_name="決算期", max_length=6, blank=True, default="",
                                       choices=f.accounting_date)
    tax_agency = models.CharField(verbose_name="管轄税務署", max_length=20, blank=True, default="", choices=f.tax_agency)
    regional_tax_office = models.CharField(verbose_name="県税事務所", max_length=20, blank=True, default="",
                                           choices=f.regional_tax_office)
    government_office = models.CharField(verbose_name="市町村役場", max_length=20, blank=True, default="",
                                         choices=f.government_office)
    business_category = models.CharField(verbose_name="事業区分", max_length=20, blank=True, default="",
                                         choices=f.business_category)
    report_category = models.CharField(verbose_name="申告区分", max_length=10, blank=True, default="",
                                       choices=f.report_category)
    consumption_tax_category = models.CharField(verbose_name="消費税区分", max_length=10, blank=True, default="",
                                                choices=f.consumption_tax_category)
    withholding_tax_method = models.CharField(verbose_name="源泉税方法", max_length=20, blank=True, default="",
                                              choices=f.withholding_tax_method)
    sales_management = models.CharField(verbose_name="売上管理先", max_length=20, blank=True, default="",
                                        choices=f.sales_management)
    report_schedule = models.CharField(verbose_name="予定申告", max_length=1, blank=True, default="", choices=f.check)
    year_adjustment_check = models.CharField(verbose_name="年末調整", max_length=1, blank=True, default="", choices=f.check)
    consumption_tax_times = models.CharField(verbose_name="消費税回数", max_length=5, blank=True, default="",
                                             choices=f.consumption_tax_times)
    depreciable_assets = models.CharField(verbose_name="償却資産", max_length=1, blank=True, default="", choices=f.check)
    extended_report = models.CharField(verbose_name="申告期限延長", max_length=1, blank=True, default="",
                                       choices=f.check)
    form_of_involvement = models.CharField(verbose_name="関与形態", max_length=20, blank=True, default="",
                                           choices=f.form_of_involvement)
    k_corporate_tax = models.CharField(verbose_name="口座振替法人税", max_length=1, blank=True, default="", choices=f.check)
    k_prefecture_tax = models.CharField(verbose_name="口座振替県民税", max_length=1, blank=True, default="", choices=f.check)
    k_city = models.CharField(verbose_name="口座振替市町村", max_length=1, blank=True, default="", choices=f.check)
    k_consumption = models.CharField(verbose_name="口座振替消費税", max_length=1, blank=True, default="", choices=f.check)
    k_income_tax = models.CharField(verbose_name="口座振替所得税", max_length=1, blank=True, default="", choices=f.check)
    report_gift_tax = models.CharField(verbose_name="贈与税申告", max_length=1, blank=True, default="", choices=f.check)
    add_memo = models.CharField(verbose_name="メモ", max_length=1, blank=True, default="", choices=f.check)
    contract_cancellation = models.CharField(verbose_name="契約解消", max_length=1, blank=True, default="", choices=f.check)
    involvement_date = models.CharField(verbose_name="関与開始日", max_length=20, blank=True, default="")  # 旧システムでは文字型のため
    create_date = models.DateField(verbose_name="作成日", auto_now_add=True)
    last_update = models.DateField(verbose_name="最終更新費", auto_now=True)
    t_filing = models.TextField(verbose_name="提出", blank=True, default="")
    t_corporate_registration = models.TextField(verbose_name="法人登記", blank=True, default="")
    t_important_points = models.TextField(verbose_name="注意事項", blank=True, default="")
    t_content = models.TextField(verbose_name="内容", blank=True, default="")
    t_start_date = models.TextField(verbose_name="開始日", blank=True, default="")
    t_end_date = models.TextField(verbose_name="終了日", blank=True, default="")
    t_history = models.TextField(verbose_name="履歴", blank=True, default="")
    content_memo = models.TextField(verbose_name="資料整理内容", blank=True, default="")
    electronic_report = models.CharField(verbose_name="電子申告", max_length=1, blank=True, default="", choices=f.check)

    def __str__(self):
        return str(self.k_number) + " " + str(self.k_name)

    class Meta:
        verbose_name_plural = "関与先名簿"


class WithholdingCheck(models.Model):
    year = models.IntegerField(verbose_name="年", )
    k_number = models.ForeignKey(ClientList, to_field='k_number',
                                 on_delete=models.DO_NOTHING, db_constraint=False, )
    type = models.CharField(verbose_name="分類", max_length=4, blank=True, default="", choices=f.type_choices)
    tax_agency = models.CharField(verbose_name="管轄税務署", max_length=20, blank=True, default="", choices=f.tax_agency)
    withholding_tax_method = models.CharField(verbose_name="源泉税方法", max_length=10, blank=True, default="")
    delivery_date = models.CharField(verbose_name="渡し日", max_length=20, blank=True, default="")
    mail_date = models.CharField(verbose_name="郵送日", max_length=20, blank=True, default="")
    note = models.CharField(verbose_name="備考", max_length=100, blank=True, default="")

    class Meta:
        verbose_name_plural = "源泉税申告チェック表"
        constraints = [
            models.UniqueConstraint(
                fields=['year', 'k_number'],
                name="year_number_withholding_check",
            )
        ]


class FilingFinalTax(models.Model):
    year = models.IntegerField(verbose_name="年", )
    k_number = models.ForeignKey(ClientList, to_field='k_number',
                                 on_delete=models.DO_NOTHING, db_constraint=False, )
    tax_agency = models.CharField(verbose_name="管轄税務署", max_length=20, blank=True, default="", choices=f.tax_agency)
    report_form_category = models.CharField(verbose_name="申告書区分", max_length=1, blank=True, default="",
                                            choices=(('', ''), ('A', 'A'), ('B', 'B')))
    report_category = models.CharField(verbose_name="申告区分", max_length=5, blank=True, default="",
                                       choices=f.report_category)
    consumption_report = models.CharField(verbose_name="消費税申告書", max_length=1, blank=True, default="", choices=f.check)
    filing = models.CharField(verbose_name="提出書", max_length=1, blank=True, default="", choices=f.check)
    sales = models.CharField(verbose_name="営業", max_length=1, blank=True, default="", choices=f.check_circle)
    agriculture = models.CharField(verbose_name="農業", max_length=1, blank=True, default="", choices=f.check_circle)
    real_estate = models.CharField(verbose_name="不動産", max_length=1, blank=True, default="", choices=f.check_circle)
    interest = models.CharField(verbose_name="利子", max_length=1, blank=True, default="", choices=f.check_circle)
    dividend = models.CharField(verbose_name="配当", max_length=1, blank=True, default="", choices=f.check_circle)
    salary = models.CharField(verbose_name="給与", max_length=1, blank=True, default="", choices=f.check_circle)
    pension = models.CharField(verbose_name="年金", max_length=1, blank=True, default="", choices=f.check_circle)
    other = models.CharField(verbose_name="その他", max_length=1, blank=True, default="", choices=f.check_circle)
    comprehensive = models.CharField(verbose_name="総合", max_length=1, blank=True, default="", choices=f.check_circle)
    separation = models.CharField(verbose_name="分離", max_length=1, blank=True, default="", choices=f.check_circle)
    temporary = models.CharField(verbose_name="一時", max_length=1, blank=True, default="", choices=f.check_circle)
    income_tax = models.CharField(verbose_name="所得税", max_length=2, blank=True, default="", choices=f.tax)
    consumption = models.CharField(verbose_name="消費税", max_length=2, blank=True, default="", choices=f.tax)
    fair_copy_date = models.CharField(verbose_name="清書終了日", max_length=5, blank=True, default="")
    seal_check_date = models.CharField(verbose_name="捺印確認日", max_length=5, blank=True, default="")
    boss_stamp_date = models.CharField(verbose_name="所長捺印日", max_length=5, blank=True, default="")
    electronic_end_date = models.CharField(verbose_name="電子送信日", max_length=5, blank=True, default="")
    attached_document_filing_date = models.CharField(verbose_name="添付書類提出日", max_length=5, blank=True, default="")
    billing_amount = models.IntegerField(verbose_name="請求額", default=0)
    withholding = models.IntegerField(verbose_name="源泉額", default=0)
    note = models.CharField(verbose_name="備考", max_length=100, blank=True, default="")
    filing2 = models.CharField(verbose_name="提出書", max_length=100, blank=True, default="")

    class Meta:
        verbose_name_plural = "確定申告"
        constraints = [
            models.UniqueConstraint(
                fields=['year', 'k_number'],
                name="year_number_filing_final_tax",
            )
        ]


class Work(models.Model):
    name = models.ForeignKey(User, to_field='username',
                             on_delete=models.DO_NOTHING, db_constraint=False, )
    date = models.DateField(verbose_name="日付", default=timezone.now)
    in_time = models.TimeField(verbose_name="出勤時間", blank=True, null=True)
    out_time = models.TimeField(verbose_name="退勤時間", blank=True, null=True)
    rest_time = models.TimeField(verbose_name="休憩時間", blank=True, null=True)
    note = models.CharField(verbose_name="備考", max_length=100, blank=True, default="")
    distance = models.FloatField(verbose_name="走行距離", default=0)

    def __str__(self):
        return str(self.name) + str(self.date)

    # @admin.display(ordering=Concat('name', Value(' '), 'date'))
    def named_date(self):
        return format_html(
            # '<span style="color: #{};">{}</span>',
            # 'ff0000',
            str(self.name.last_name) + str(self.name.first_name) + ' ' + str(self.date),
        )

    @property
    def sum(self):
        a = datetime.timedelta(hours=self.out_time.hour, minutes=self.out_time.minute) - \
            datetime.timedelta(hours=self.in_time.hour, minutes=self.in_time.minute) - \
            datetime.timedelta(hours=self.rest_time.hour)
        a = round(a.total_seconds())
        b = str(a % 3600 // 60) if len(str(a % 3600 // 60)) == 2 else str(a % 3600 // 60) + "0"
        c = str(a // 3600) + ":" + b if len(b) == 2 else b + "0"
        return c

    def w(self):
        return datetime.date(year=self.date.year, month=self.date.month, day=self.date.day).strftime('%a')

    class Meta:
        verbose_name_plural = "出勤表"
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'date'],
                name="name_date_work",
            )
        ]


class YearAdjustment(models.Model):
    year = models.IntegerField(verbose_name="年", )
    k_number = models.ForeignKey(ClientList, to_field='k_number',
                                 on_delete=models.DO_NOTHING, db_constraint=False, )
    tax_agency = models.CharField(verbose_name="管轄税務署", max_length=20, blank=True, default="", choices=f.tax_agency)
    year_adjustment_day = models.CharField(verbose_name="年末調整日", max_length=6, blank=True, default="")
    personnel = models.IntegerField(verbose_name="調整人員", default=0)
    city_paper = models.IntegerField(verbose_name="紙", default=0)
    city_electronic = models.IntegerField(verbose_name="電子", default=0)
    star = models.CharField(verbose_name="★", max_length=1, blank=True, choices=(('', ''), ('★', '★')))
    payment_create_date = models.CharField(verbose_name="支払書作成日", max_length=6, blank=True, default="")
    date = models.CharField(verbose_name="完了日", max_length=6, blank=True, default="")
    payment_slip_delivery = models.CharField(verbose_name="納付書渡し日", max_length=6, blank=True, default="")
    payment_slip_mail = models.CharField(verbose_name="納付書郵送日", max_length=6, blank=True, default="")
    billing_amount = models.IntegerField(verbose_name="請求額", default=0)
    withholding_tax = models.IntegerField(verbose_name="源泉税", default=0)
    invoice_number = models.CharField(verbose_name="請求書番号", max_length=6, blank=True, default="")
    report_create_date = models.CharField(verbose_name="申告書作成日", max_length=6, blank=True, default="")
    filing_date = models.CharField(verbose_name="提出完了日", max_length=6, blank=True, default="")
    electronic_or_paper = models.CharField(verbose_name="電子または紙", max_length=2, blank=True, default="",
                                           choices=f.electronic_or_paper)
    billing_amount2 = models.IntegerField(verbose_name="請求額", default=0)
    withholding_tax2 = models.IntegerField(verbose_name="源泉税", default=0)
    note = models.CharField(verbose_name="備考", max_length=100, blank=True, default="")

    class Meta:
        verbose_name_plural = "年末調整"
        constraints = [
            models.UniqueConstraint(
                fields=['year', 'k_number'],
                name="year_number_year_adjustment",
            )
        ]


class Invoice(models.Model):
    k_number = models.ForeignKey(ClientList, to_field='k_number',
                                 on_delete=models.DO_NOTHING, db_constraint=False, )
    date = models.DateField(verbose_name="日付", blank=True, default=timezone.now)
    reward = models.CharField(verbose_name="報酬", max_length=100, blank=True, default="")
    items = models.CharField(verbose_name="内訳", max_length=100, blank=True, default="")
    money = models.IntegerField(verbose_name="金額", default=0)
    consumption = models.IntegerField(verbose_name="消費税", default=0)
    withholding_income_tax = models.IntegerField(verbose_name="源泉所得税", default=0)
    reconstruction_tax = models.IntegerField(verbose_name="特別復興税", default=0)

    class Meta:
        verbose_name_plural = "請求書"


class Memo(models.Model):
    k_number = models.ForeignKey(ClientList, to_field='k_number',
                                 on_delete=models.DO_NOTHING, db_constraint=False, )
    content_memo = models.TextField(verbose_name="", blank=True, default="")

    class Meta:
        verbose_name_plural = "資料整理"


class FilingFormList(models.Model):
    year = models.IntegerField(verbose_name="年", )
    month = models.CharField(verbose_name="月", max_length=6, blank=True, choices=f.accounting_date)
    k_number = models.ForeignKey(ClientList, to_field='k_number',
                                 on_delete=models.DO_NOTHING, db_constraint=False, verbose_name='test')
    tax_agency = models.CharField(verbose_name="管轄税務署", max_length=20, blank=True, default="", choices=f.tax_agency)
    regional_tax_office = models.CharField(verbose_name="県税事務所", max_length=100, blank=True, default="",
                                           choices=f.regional_tax_office)
    government_office = models.CharField(verbose_name="市町村役場", max_length=100, blank=True, default="",
                                         choices=f.government_office)
    accounting_date = models.CharField(verbose_name="決算期", max_length=10, blank=True, default="",
                                       choices=f.accounting_date)
    consumption_tax_category = models.CharField(verbose_name="消費税区分", max_length=10, blank=True, default="",
                                                choices=f.consumption_tax_category)
    consumption_tax_times = models.CharField(verbose_name="消費税回数", max_length=10, blank=True, default="",
                                             choices=f.consumption_tax_times)
    report_schedule = models.CharField(verbose_name="予定申告", max_length=1, blank=True, default="",
                                       choices=f.check)
    document1 = models.CharField(verbose_name="書類1", max_length=20, blank=True, default="", choices=f.document_choices1)
    document2 = models.CharField(verbose_name="書類2", max_length=20, blank=True, default="", choices=f.document_choices2)
    tax_agency_note = models.CharField(verbose_name="管轄税務署備考", max_length=20, blank=True, default="",
                                       choices=f.tax_agency_note_choices)
    regional_tax_office_note = models.CharField(verbose_name="県税事務所備考", max_length=20, blank=True, default="",
                                                choices=f.regional_tax_office_note_choices)
    government_office_note = models.CharField(verbose_name="市町村役場備考", max_length=20, blank=True, default="",
                                              choices=f.government_office_note_choices)
    report_schedule_note = models.CharField(verbose_name="予定申告備考", max_length=20, blank=True, default="")
    consumption_tax_times_note = models.CharField(verbose_name="消費税予定回数備考", max_length=20, blank=True, default="")
    insert_date = models.DateField(verbose_name="送信日", blank=True, null=True)
    insert_date_note = models.CharField(verbose_name="送信日備考", max_length=20, blank=True, default="")
    accounting_date_consumption_tax_category = models.CharField(max_length=20)

    @property
    def get_accounting_date_consumption_tax_category(self):
        return str(self.accounting_date) + str(self.consumption_tax_category)

    def save(self, *args, **kwargs):
        self.accounting_date_consumption_tax_category = self.get_accounting_date_consumption_tax_category
        super(FilingFormList, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "提出一覧"
        constraints = [
            models.UniqueConstraint(
                fields=['year', 'month', 'k_number'],
                name="year_month_number_filing_form_list",
            )
        ]


class SalesManagement(models.Model):
    year = models.IntegerField(verbose_name="年", )
    k_number = models.ForeignKey(ClientList, to_field='k_number',
                                 on_delete=models.DO_NOTHING, db_constraint=False, )
    m1 = models.IntegerField(verbose_name="1月", default=0)
    m2 = models.IntegerField(verbose_name="2月", default=0)
    m3 = models.IntegerField(verbose_name="3月", default=0)
    m4 = models.IntegerField(verbose_name="4月", default=0)
    m5 = models.IntegerField(verbose_name="5月", default=0)
    m6 = models.IntegerField(verbose_name="6月", default=0)
    m7 = models.IntegerField(verbose_name="7月", default=0)
    m8 = models.IntegerField(verbose_name="8月", default=0)
    m9 = models.IntegerField(verbose_name="9月", default=0)
    m10 = models.IntegerField(verbose_name="10月", default=0)
    m11 = models.IntegerField(verbose_name="11月", default=0)
    m12 = models.IntegerField(verbose_name="12月", default=0)
    first_term = models.IntegerField(verbose_name="前期未収", default=0)
    current_term = models.IntegerField(verbose_name="当期未収", default=0)

    class Meta:
        verbose_name_plural = "売上管理表"
        constraints = [
            models.UniqueConstraint(
                fields=['year', 'k_number'],
                name="year_number_sales_management",
            )
        ]


class OfficerChange(models.Model):
    year = models.IntegerField(verbose_name="年", )
    k_number = models.ForeignKey(ClientList, to_field='k_number',
                                 on_delete=models.DO_NOTHING, db_constraint=False, )
    note = models.CharField(verbose_name="備考", max_length=100, blank=True, default="")

    class Meta:
        verbose_name_plural = "役員変更"
        constraints = [
            models.UniqueConstraint(
                fields=['year', 'k_number'],
                name="year_number_officer_change",
            )
        ]


class GiftTax(models.Model):
    year = models.IntegerField(verbose_name="年", )
    k_number = models.ForeignKey(ClientList, to_field='k_number',
                                 on_delete=models.DO_NOTHING, db_constraint=False, )
    tax_agency = models.CharField(verbose_name="管轄税務署", max_length=20, blank=True, default="", choices=f.tax_agency)
    return_date = models.CharField(verbose_name="返却日付", max_length=5, blank=True, default="")
    end_date = models.CharField(verbose_name="終了日付", max_length=5, blank=True, default="")
    payment_slip_exist = models.CharField(verbose_name="納付書", max_length=1, blank=True, default="", choices=f.check)
    payment_slip_date = models.CharField(verbose_name="納付書日付", max_length=5, blank=True, default="")
    report_create_date = models.CharField(verbose_name="申告書作成日", max_length=5, blank=True, default="")
    fair_copy_date = models.CharField(verbose_name="清書終了日", max_length=5, blank=True, default="")
    boss_stamp_date = models.CharField(verbose_name="所長捺印日", max_length=5, blank=True, default="")
    client_stamp_date = models.CharField(verbose_name="納税者捺印日", max_length=5, blank=True, default="")
    filing_date = models.CharField(verbose_name="申告書提出日", max_length=5, blank=True, default="")
    electronic_or_paper = models.CharField(verbose_name="電子または紙", max_length=2, blank=True, default="",
                                           choices=f.electronic_or_paper)
    reward_billing_amount = models.IntegerField(verbose_name="報酬請求額", default=0)
    reward_withholding = models.IntegerField(verbose_name="報酬厳選額", default=0)
    copy1 = models.CharField(verbose_name="コピー", max_length=1, blank=True, default="", choices=f.check_circle)
    note = models.CharField(verbose_name="備考", max_length=100, blank=True, default="")

    class Meta:
        verbose_name_plural = "贈与税申告申告チェック表"
        constraints = [
            models.UniqueConstraint(
                fields=['year', 'k_number'],
                name="year_number_gift_tax",
            )
        ]


class ScheduleBox(models.Model):
    k_number = models.ForeignKey(ClientList, to_field='k_number',
                                 on_delete=models.DO_NOTHING, db_constraint=False, )
    date = models.DateField(verbose_name="日付", blank=True, default=timezone.now)
    filing_type = models.CharField(verbose_name="提出", max_length=2, default="予定",
                                   choices=(('予定', '予定'), ('済み', '済み')))
    content = models.TextField(verbose_name="内容", blank=True, default="")
    note = models.CharField(verbose_name="備考", max_length=100, blank=True, default="")

    class Meta:
        verbose_name_plural = "提出予定"
        constraints = [
            models.UniqueConstraint(
                fields=['k_number', 'date'],
                name="number_date_schedule_box",
            )
        ]


class DirectPayment(models.Model):
    year = models.IntegerField(verbose_name="年", )
    k_number = models.ForeignKey(ClientList, to_field='k_number',
                                 on_delete=models.DO_NOTHING, db_constraint=False, )
    tax_type = models.CharField(verbose_name="税種類", max_length=10, blank=True, default="", choices=f.tax_type)
    m1 = models.CharField(verbose_name="1月", max_length=10, blank=True, default="")
    m2 = models.CharField(verbose_name="2月", max_length=10, blank=True, default="")
    m3 = models.CharField(verbose_name="3月", max_length=10, blank=True, default="")
    m4 = models.CharField(verbose_name="4月", max_length=10, blank=True, default="")
    m5 = models.CharField(verbose_name="5月", max_length=10, blank=True, default="")
    m6 = models.CharField(verbose_name="6月", max_length=10, blank=True, default="")
    m7 = models.CharField(verbose_name="7月", max_length=10, blank=True, default="")
    m8 = models.CharField(verbose_name="8月", max_length=10, blank=True, default="")
    m9 = models.CharField(verbose_name="9月", max_length=10, blank=True, default="")
    m10 = models.CharField(verbose_name="10月", max_length=10, blank=True, default="")
    m11 = models.CharField(verbose_name="11月", max_length=10, blank=True, default="")
    m12 = models.CharField(verbose_name="12月", max_length=10, blank=True, default="")

    class Meta:
        verbose_name_plural = "ダイレクト納付"
        constraints = [
            models.UniqueConstraint(
                fields=['year', 'k_number_id'],
                name="year_number_direct_payment",
            )
        ]
