from django import forms
import datetime
from diary import forms_choices as f
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.utils.translation import gettext_lazy as _
import environ

env = environ.Env()
global_year = forms.IntegerField(label='年', max_value=3000, min_value=1, initial=datetime.datetime.now().year)
global_number = forms.IntegerField(label='番号', max_value=100000, min_value=1, required=False)
global_number_choice = forms.ChoiceField(label='番号', choices=(('', ''),), required=False,
                                         widget=forms.Select(attrs={'class': 'form_height', 'placeholder': '番号 名前'}))
global_number_table = forms.IntegerField(label='番号', max_value=100000, min_value=1, required=False,
                                         widget=forms.NumberInput(attrs={'class': 'td_mid_int'}))
global_k_name = forms.CharField(label='顧問先名', required=False)
global_k_name_table = forms.CharField(label='顧問先名', required=False,
                                      widget=forms.Textarea(attrs={'cols': '20', 'rows': '1', 'class': 'td_name'}))
global_name = forms.ChoiceField(label='名前', choices=f.users)
global_manager = forms.ChoiceField(label='担当者', choices=f.manager, required=False)
global_note = forms.CharField(label='備考', max_length=100, required=False)
global_note_table = forms.CharField(label='備考', max_length=100, required=False,
                                    widget=forms.Textarea(attrs={'cols': '6', 'rows': '1', 'class': 'td_menu'}))
global_char = forms.CharField(label='文字型', max_length=100, min_length=0, required=False)
global_int = forms.IntegerField(label='整数型', max_value=100000, min_value=0, required=False)
global_tax_agency = forms.ChoiceField(label='管轄税務署', choices=f.tax_agency, required=False)
global_tax_agency_table = forms.ChoiceField(label='管轄<br>税務署', choices=f.tax_agency, required=False,
                                            widget=forms.Select(attrs={'cols': '2', 'rows': '1', 'class': 'td_note'}))

withholding_tax2 = forms.IntegerField(label='源泉税', max_value=100000, required=False,
                                      widget=forms.Textarea(
                                          attrs={'cols': '6', 'rows': '1', 'class': 'td_form'}))


class YearForm(forms.Form):
    year = global_year


class YearMonthForm(forms.Form):
    year = global_year
    month = forms.ChoiceField(label='月', choices=f.accounting_date)


class YearMonthNumberForm(forms.Form):
    year = global_year
    month = forms.ChoiceField(label='月', choices=f.accounting_date)
    number = global_number
    number_choice = global_number_choice


class YearManageTaxAgencyForm(forms.Form):
    year = global_year
    manager = global_manager
    tax_agency = global_tax_agency


class YearTaxAgencyTypeForm(forms.Form):
    year = global_year
    tax_agency = global_tax_agency
    type = forms.ChoiceField(label='分類', choices=f.type_choices)


class YearNumberForm(forms.Form):
    year = global_year
    number = global_number
    number_choice = global_number_choice


class ClientInputForm(forms.Form):
    number = forms.IntegerField(label='顧問先番号', min_value=1, max_value=100000)
    number_choice = forms.ChoiceField(label='顧問先番号')
    type = forms.ChoiceField(label='分類', choices=f.type_choices)


class ClientDetailForm(forms.Form):
    type = forms.ChoiceField(label='分類', choices=f.type_choices)
    k_number = forms.IntegerField(label='顧問先番号', max_value=100000)
    k_ruby = forms.CharField(label='フリガナ1', max_length=100, required=False)
    k_name = forms.CharField(label='顧問先名', max_length=100)
    company_name = forms.CharField(label='屋号または会社名', max_length=100, required=False)
    post_number = forms.CharField(label='所在地（郵便番号）', max_length=100, required=False)
    prefecture = forms.ChoiceField(label='都道府県', choices=f.prefecture, required=False)
    city = forms.CharField(label='市町村', max_length=100, required=False,
                           widget=forms.Textarea(attrs={'rows': '2', 'class': 'form_resize_none'}))
    tell_number = forms.CharField(label='電話番号', max_length=100, required=False)
    fax_number = forms.CharField(label='FAX番号', max_length=100, required=False)
    representative_ruby = forms.CharField(label='フリガナ2', max_length=100, required=False)
    representative_mei = forms.CharField(label='代表者名', max_length=100, required=False)
    representative_post_number = forms.CharField(label='代表者郵便番号', max_length=100, required=False)
    representative_address = forms.CharField(label='代表者住所', max_length=100, required=False)
    manager1 = forms.ChoiceField(label='担当者1', choices=f.manager, required=False)
    manager2 = forms.ChoiceField(label='担当者2', choices=f.manager, required=False)
    manager_check = forms.ChoiceField(label='担当者チェック', choices=f.check, required=False)
    accounting_date = forms.ChoiceField(label='決算期', choices=f.accounting_date, required=False)
    tax_agency = forms.ChoiceField(label='管轄税務署', choices=f.tax_agency, required=False)
    regional_tax_office = forms.ChoiceField(label='県税事務所', choices=f.regional_tax_office, required=False)
    government_office = forms.ChoiceField(label='市町村役場', choices=f.government_office, required=False)
    business_category = forms.ChoiceField(label='(旧)事業区分', choices=f.business_category, required=False)
    report_category = forms.ChoiceField(label='申告区分', choices=f.report_category, required=False)
    consumption_tax_category = forms.ChoiceField(label='消費税申告区分', choices=f.consumption_tax_category, required=False)
    withholding_tax_method = forms.ChoiceField(label='源泉税納付方法', choices=f.withholding_tax_method, required=False)
    sales_management = forms.ChoiceField(label='売上管理先', choices=f.sales_management, required=False)
    report_schedule = forms.ChoiceField(label='予定申告', choices=f.check, required=False)
    year_adjustment_check = forms.ChoiceField(label='年末調整', choices=f.check, required=False)
    consumption_tax_times = forms.ChoiceField(label='消費税予定回数', choices=f.consumption_tax_times, required=False)
    depreciable_assets = forms.ChoiceField(label='償却資産申告', choices=f.check, required=False)
    extended_report = forms.ChoiceField(label='申告期限の延長', choices=f.check, required=False)
    form_of_involvement = forms.ChoiceField(label='関与形態', choices=f.form_of_involvement, required=False)
    k_corporate_tax = forms.ChoiceField(label='口座振替法人税', choices=f.check_circle, required=False)
    k_prefecture_tax = forms.ChoiceField(label='口座振替県民税', choices=f.check_circle, required=False)
    k_city = forms.ChoiceField(label='口座振替市町村', choices=f.check_circle, required=False)
    k_consumption = forms.ChoiceField(label='口座振替消費税', choices=f.check_circle, required=False)
    k_income_tax = forms.ChoiceField(label='口座振替所得税', choices=f.check_circle, required=False)
    report_gift_tax = forms.ChoiceField(label='贈与税申告', choices=f.check_circle, required=False)
    add_memo = forms.ChoiceField(label='メモに追加', choices=f.check, required=False)
    contract_cancellation = forms.ChoiceField(label='契約解消', choices=f.check, required=False)
    involvement_date = forms.CharField(label='関与開始日', max_length=100, required=False)
    create_date = forms.DateField(label='作成日', required=False)
    last_update = forms.DateField(label='最終更新', required=False)
    t_filing = forms.CharField(label='(旧)提出書類', max_length=10000, required=False,
                               widget=forms.Textarea(attrs={'rows': '7', 'columns': '20'}))
    t_corporate_registration = forms.CharField(label='法人登記関係', max_length=10000, required=False)
    t_important_points = forms.CharField(label='決算注意事項', max_length=10000, required=False)
    t_content = forms.CharField(label='税務調査内容', max_length=10000, required=False)
    t_start_date = forms.CharField(label='税務調査開始日', max_length=10000, required=False)
    t_end_date = forms.CharField(label='税務調査終了日', max_length=10000, required=False)
    t_history = forms.CharField(label='税務調査履歴', max_length=10000, required=False)
    content_memo = forms.CharField(label='資料整理内容', max_length=10000, required=False)
    electronic_report = forms.ChoiceField(label='電子申告の有無', choices=f.check, required=False)

class ScheduleBoxForm(forms.Form):
    number = global_number
    number_choice = global_number_choice
    date = forms.DateField(label='送信日',
                           initial=datetime.datetime.now(),
                           widget=forms.DateInput(attrs={"type": "date"}))
    filing_type = forms.ChoiceField(label='提出', required=False,
                                    choices=(('予定', '予定'), ('済み', '済み'),),
                                    widget=forms.Select(attrs={'class': 'form_height'}))
    content = forms.CharField(label='内容', max_length=100, required=False,
                              widget=forms.Textarea(attrs={'rows': '7', 'class': 'form_resize_none'}))
    note = global_note


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.Select(choices=f.users))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        initial=env('USER_PASSWORD'),
    )


class DirectPaymentForm(forms.Form):
    year = global_year
    number = global_number
    number_choice = global_number_choice
    k_name = global_k_name
    tax_type = forms.ChoiceField(label='税種類', choices=f.tax_type)
    month_widget = forms.Textarea(attrs={'cols': '6', 'rows': '1', 'class': 'form_resize_none'})
    m1 = forms.CharField(label='1月', max_length=5, required=False, widget=month_widget)
    m2 = forms.CharField(label='2月', max_length=5, required=False, widget=month_widget)
    m3 = forms.CharField(label='3月', max_length=5, required=False, widget=month_widget)
    m4 = forms.CharField(label='4月', max_length=5, required=False, widget=month_widget)
    m5 = forms.CharField(label='5月', max_length=5, required=False, widget=month_widget)
    m6 = forms.CharField(label='6月', max_length=5, required=False, widget=month_widget)
    m7 = forms.CharField(label='7月', max_length=5, required=False, widget=month_widget)
    m8 = forms.CharField(label='8月', max_length=5, required=False, widget=month_widget)
    m9 = forms.CharField(label='9月', max_length=5, required=False, widget=month_widget)
    m10 = forms.CharField(label='10月', max_length=5, required=False, widget=month_widget)
    m11 = forms.CharField(label='11月', max_length=5, required=False, widget=month_widget)
    m12 = forms.CharField(label='12月', max_length=5, required=False, widget=month_widget)


class FilingForm(forms.Form):
    number = global_number_table
    k_name = forms.CharField(label='顧問先名', required=False,
                             widget=forms.Textarea(attrs={'cols': '20', 'rows': '1', 'class': 'td_name'}))
    document1 = forms.ChoiceField(label='申告種類<br>提出書類', choices=f.document_choices1, required=False,
                                  widget=forms.Select(attrs={'cols': '2', 'rows': '1', 'class': 'td_note'}))
    tax_agency = global_tax_agency_table
    regional_tax_office = forms.ChoiceField(label='県税<br>事務所', choices=f.regional_tax_office, required=False,
                                            widget=forms.Select(
                                                attrs={'cols': '6', 'rows': '1', 'class': 'td_note'}))
    government_office = forms.ChoiceField(label='市町村<br>役場', choices=f.government_office, required=False,
                                          widget=forms.Select(
                                              attrs={'cols': '6', 'rows': '1', 'class': 'td_note'}))
    report_schedule = forms.ChoiceField(label='予定申告', choices=f.check, required=False,
                                        widget=forms.Select(attrs={'cols': '2', 'rows': '1', 'class': 'td_menu2'}))
    consumption_tax_times = forms.ChoiceField(label='消費税<br>予定回数', choices=f.consumption_tax_times, required=False,
                                              widget=forms.Select(
                                                  attrs={'cols': '2', 'rows': '1', 'class': 'td_menu2'}))

    insert_date = forms.DateField(label='送信日', required=False,
                                  initial=datetime.datetime.now(),
                                  widget=forms.DateInput(attrs={"type": "date", 'class': 'td_note'}))



class FilingForm2(forms.Form):
    accounting_date = forms.ChoiceField(label='決算期', choices=f.accounting_date,
                                        widget=forms.Select(attrs={'cols': '2', 'rows': '1', 'class': 'td_form'}))
    consumption_tax_category = forms.ChoiceField(label='消費税<br>区分', choices=f.consumption_tax_category, required=False,
                                                 widget=forms.Select(
                                                     attrs={'cols': '2', 'rows': '1', 'class': 'td_form'}))
    document2 = forms.ChoiceField(label='書類2', choices=f.document_choices2, required=False,
                                  widget=forms.Select(attrs={'cols': '2', 'rows': '1', 'class': 'td_form'}))
    tax_agency_note = forms.ChoiceField(label='管轄備考', choices=f.tax_agency_note_choices, required=False,
                                        widget=forms.Select(attrs={'cols': '2', 'rows': '1', 'class': 'td_form'}))
    regional_tax_office_note = forms.ChoiceField(label='県税事務所<br>備考', choices=f.regional_tax_office_note_choices,
                                                 required=False,
                                                 widget=forms.Select(
                                                     attrs={'cols': '2', 'rows': '1', 'class': 'td_form'}))
    government_office_note = forms.ChoiceField(label='市町村役場<br>備考', choices=f.government_office_note_choices,
                                               required=False,
                                               widget=forms.Select(
                                                   attrs={'cols': '2', 'rows': '1', 'class': 'td_note'}))
    report_schedule_note = forms.CharField(label='予定申告<br>備考', max_length=20, required=False,
                                           widget=forms.Textarea(
                                               attrs={'cols': '6', 'rows': '1', 'class': 'td_menu2'}))
    consumption_tax_times_note = forms.CharField(label='消費税<br>予定回数備考', max_length=20, required=False,
                                                 widget=forms.Textarea(
                                                     attrs={'cols': '6', 'rows': '1', 'class': 'td_menu2'}))
    insert_date_note = forms.CharField(label='送信日<br>備考', max_length=100, required=False,
                                       widget=forms.Textarea(
                                           attrs={'cols': '6', 'rows': '1', 'class': 'td_menu2'}))


class MainForm(forms.Form):
    username = global_name


class WithholdingForm(forms.Form):
    number = global_number
    k_name = global_k_name
    type = forms.ChoiceField(label='分類', choices=f.type_choices,
                             widget=forms.Select(attrs={'cols': '2', 'rows': '1', 'class': 'td_menu2'}))
    tax_agency = forms.ChoiceField(label='管轄<br>税務署', choices=f.tax_agency, required=False,
                                   widget=forms.Select(attrs={'cols': '2', 'rows': '1', 'class': 'td_menu2'}))
    withholding_tax_method = forms.CharField(label='源泉税<br>納付方法', max_length=10, required=False,
                                             widget=forms.Textarea(
                                                 attrs={'cols': '6', 'rows': '1', 'class': 'td_note'}))
    delivery_date = forms.DateField(label='納付書<br>渡し日', required=False,
                                    widget=forms.DateInput(attrs={"type": "date", 'class': 'td_note'}))
    mail_date = forms.DateField(label='納付書<br>郵送日', required=False,
                                widget=forms.DateInput(attrs={"type": "date", 'class': 'td_note'}))
    note = global_note_table


class SalesManagementForm(forms.Form):
    year = global_year
    bank = forms.ChoiceField(label='銀行名', choices=f.sales_management)
    number = global_number
    number_choice = global_number_choice
    k_name = global_k_name
    sales_withhold = forms.ChoiceField(label='売上表または源泉税表', choices=(('売上', '売上'), ('源泉税', '源泉税')))
    m1 = forms.IntegerField(label='1月', max_value=1000000000, min_value=0, required=False, )
    m2 = forms.IntegerField(label='2月', max_value=1000000000, min_value=0, required=False)
    m3 = forms.IntegerField(label='3月', max_value=1000000000, min_value=0, required=False)
    m4 = forms.IntegerField(label='4月', max_value=1000000000, min_value=0, required=False)
    m5 = forms.IntegerField(label='5月', max_value=1000000000, min_value=0, required=False)
    m6 = forms.IntegerField(label='6月', max_value=1000000000, min_value=0, required=False)
    m7 = forms.IntegerField(label='7月', max_value=1000000000, min_value=0, required=False)
    m8 = forms.IntegerField(label='8月', max_value=1000000000, min_value=0, required=False)
    m9 = forms.IntegerField(label='9月', max_value=1000000000, min_value=0, required=False)
    m10 = forms.IntegerField(label='10月', max_value=1000000000, min_value=0, required=False)
    m11 = forms.IntegerField(label='11月', max_value=1000000000, min_value=0, required=False)
    m12 = forms.IntegerField(label='12月', max_value=1000000000, min_value=0, required=False)
    first_term = forms.IntegerField(label='前期未収', max_value=1000000000, min_value=0, required=False)
    current_term = forms.IntegerField(label='当期未収', max_value=1000000000, min_value=0, required=False)
    kei = forms.IntegerField(label='合計当期未収', max_value=1000000000, min_value=0, required=False)


class FilingFinalTaxForm(forms.Form):
    number = global_number_table
    k_name = global_k_name_table
    report_form_category = forms.ChoiceField(label='申告書<br>区分', choices=(('', ''), ('A', 'A'), ('B', 'B')),
                                             required=False, widget=forms.Select(attrs={'class': 'td_menu'}))
    report_category = forms.ChoiceField(label='申告<br>区分', choices=f.report_category,
                                        required=False, widget=forms.Select(attrs={'class': 'td_form'}))
    consumption_report = forms.ChoiceField(label='消費税<br>申告書', choices=f.check, required=False,
                                           widget=forms.Select(attrs={'cols': '6', 'rows': '1', 'class': 'td_menu'}))
    filing = forms.ChoiceField(label='提出書', choices=f.check, required=False,
                               widget=forms.Select(attrs={'cols': '6', 'rows': '1', 'class': 'td_menu'}))
    sales = forms.Field(label="営業", required=False, widget=forms.CheckboxInput(attrs={'value': '○', 'class': 'td_box'}))
    agriculture = forms.Field(label="農業", required=False,
                              widget=forms.CheckboxInput(attrs={'value': '○', 'class': 'td_box'}))
    real_estate = forms.Field(label="不動<br>産", required=False,
                              widget=forms.CheckboxInput(attrs={'value': '○', 'class': 'td_box'}))
    interest = forms.Field(label="利子", required=False,
                           widget=forms.CheckboxInput(attrs={'value': '○', 'class': 'td_box'}))
    dividend = forms.Field(label="配当", required=False,
                           widget=forms.CheckboxInput(attrs={'value': '○', 'class': 'td_box'}))
    salary = forms.Field(label="給与", required=False,
                         widget=forms.CheckboxInput(attrs={'value': '○', 'class': 'td_box'}))
    pension = forms.Field(label="年金", required=False,
                          widget=forms.CheckboxInput(attrs={'value': '○', 'class': 'td_box'}))
    other = forms.Field(label="他　", required=False,
                        widget=forms.CheckboxInput(attrs={'value': '○', 'class': 'td_box'}))
    comprehensive = forms.Field(label="総合", required=False,
                                widget=forms.CheckboxInput(attrs={'value': '○', 'class': 'td_box'}))
    separation = forms.Field(label="分離", required=False,
                             widget=forms.CheckboxInput(attrs={'value': '○', 'class': 'td_box'}))
    temporary = forms.Field(label="一時", required=False,
                            widget=forms.CheckboxInput(attrs={'value': '○', 'class': 'td_box'}))
    income_tax = forms.ChoiceField(label='所得税', choices=f.tax, required=False,
                                   widget=forms.Textarea(
                                       attrs={'cols': '6', 'rows': '1', 'class': 'td_menu'}))
    consumption = forms.ChoiceField(label='消費税', choices=f.tax, required=False,
                                    widget=forms.Textarea(
                                        attrs={'cols': '6', 'rows': '1', 'class': 'td_menu'}))
    fair_copy_date = forms.CharField(label='納税者<br>捺印確認', max_length=5, required=False,
                                     widget=forms.Textarea(
                                         attrs={'cols': '6', 'rows': '1', 'class': 'td_menu'}))
    seal_check_date = forms.CharField(label='納税者<br>捺印確認', max_length=5, required=False,
                                      widget=forms.Textarea(
                                          attrs={'cols': '6', 'rows': '1', 'class': 'td_menu'}))
    boss_stamp_date = forms.CharField(label='所長<br>捺印日', max_length=5, required=False,
                                      widget=forms.Textarea(
                                          attrs={'cols': '6', 'rows': '1', 'class': 'td_menu'}))
    electronic_end_date = forms.CharField(label='電子申告<br>送信日', max_length=5, required=False,
                                          widget=forms.Textarea(
                                              attrs={'cols': '6', 'rows': '1', 'class': 'td_menu'}))
    attached_document_filing_date = forms.CharField(label='申告書<br>添付書類<br>提出日', max_length=5, required=False,
                                                    widget=forms.Textarea(
                                                        attrs={'cols': '6', 'rows': '1', 'class': 'td_menu'}))
    billing_amount = forms.IntegerField(label='報酬<br>請求額', max_value=1000000, initial=0,
                                        widget=forms.NumberInput(attrs={'class': 'td_short_int'}))
    withholding = forms.IntegerField(label='報酬<br>源泉額', max_value=100000, initial=0,
                                     widget=forms.NumberInput(attrs={'class': 'td_short_int'}))
    note = global_note_table
    filing2 = forms.CharField(label='提出書内容<br>「,」で区切る', max_length=1000, required=False,
                              widget=forms.Textarea(attrs={'cols': '6', 'rows': '1', 'class': 'td_note'}))


class YearAdjustmentForm(forms.Form):
    number = global_number_table
    k_name = global_k_name_table
    year_adjustment_day = forms.CharField(label='年末<br>調整日', max_length=5, required=False,
                                          widget=forms.Textarea(
                                              attrs={'cols': '6', 'rows': '1', 'class': 'td_form'}))
    personnel = forms.IntegerField(label='調整<br>人員', max_value=100, required=False,
                                   widget=forms.NumberInput(attrs={'class': 'td_short_int'}))
    city_paper = forms.IntegerField(label='紙', max_value=100, required=False,
                                    widget=forms.NumberInput(attrs={'class': 'td_short_int'}))
    city_electronic = forms.IntegerField(label='電子', max_value=100, required=False,
                                         widget=forms.NumberInput(attrs={'class': 'td_short_int'}))
    star = forms.ChoiceField(label='★', choices=(('', ''), ('★', '★')), required=False,
                             widget=forms.Select(
                                 attrs={'cols': '2', 'rows': '1', 'class': 'td_form'}))
    payment_create_date = forms.CharField(label='支払合計<br>表作成日', max_length=5, required=False,
                                          widget=forms.Textarea(
                                              attrs={'cols': '6', 'rows': '1', 'class': 'td_form'}))
    date = forms.CharField(label='提出<br>完了日', max_length=5, required=False,
                           widget=forms.Textarea(
                               attrs={'cols': '6', 'rows': '1', 'class': 'td_form'}))
    payment_slip_delivery = forms.CharField(label='納付書<br>渡し', max_length=5, required=False,
                                            widget=forms.Textarea(
                                                attrs={'cols': '6', 'rows': '1', 'class': 'td_form'}))
    payment_slip_mail = forms.CharField(label='納付書<br>郵送', max_length=5, required=False,
                                        widget=forms.Textarea(
                                            attrs={'cols': '6', 'rows': '1', 'class': 'td_form'}))
    billing_amount = forms.IntegerField(label='請求額<br>（税抜）', max_value=1000000, required=False,
                                        widget=forms.NumberInput(attrs={'class': 'td_int'}))
    withholding_tax = forms.IntegerField(label='源泉税', max_value=100000, required=False,
                                         widget=forms.NumberInput(attrs={'class': 'td_int'}))
    invoice_number = forms.CharField(label='請求書<br>No', max_length=20, required=False,
                                     widget=forms.Textarea(
                                         attrs={'cols': '6', 'rows': '1', 'class': 'td_form'}))
    report_create_date = forms.CharField(label='申告書<br>作成日', max_length=5, required=False,
                                         widget=forms.Textarea(
                                             attrs={'cols': '6', 'rows': '1', 'class': 'td_form'}))
    filing_date = forms.CharField(label='償却資産<br>提出日', max_length=5, required=False,
                                  widget=forms.Textarea(
                                      attrs={'cols': '6', 'rows': '1', 'class': 'td_form'}))
    electronic_or_paper = forms.ChoiceField(label='電子<br>紙', choices=f.electronic_or_paper, required=False,
                                            widget=forms.Select(
                                                attrs={'cols': '2', 'rows': '1', 'class': 'td_form'}))
    billing_amount2 = forms.IntegerField(label='請求額<br>（税抜）', max_value=1000000, required=False,
                                         widget=forms.NumberInput(attrs={'class': 'td_int'}))
    withholding_tax2 = forms.IntegerField(label='源泉税', max_value=100000, required=False,
                                          widget=forms.NumberInput(attrs={'class': 'td_int'}))
    note = global_note_table


class OfficerChangeForm(forms.Form):
    number = global_number
    number_choice = global_number_choice
    year = global_year
    note = global_note


class MemoForm(forms.Form):
    name = global_manager
    number = global_number
    number_choice = global_number_choice
    content = forms.CharField(label='内容', max_length=1000, required=False)


class GiftTaxCheckForm(forms.Form):
    number = global_number
    k_name = global_k_name
    tax_agency = global_tax_agency_table
    electronic_or_paper = forms.ChoiceField(label="電子紙", choices=f.electronic_or_paper, required=False,
                                            widget=forms.Select(attrs={'cols': '2', 'rows': '1', 'class': 'td_form'}))
    return_date = forms.CharField(label="返却日", max_length=5, required=False,
                                  widget=forms.Textarea(
                                      attrs={'cols': '6', 'rows': '1', 'class': 'td_menu'}))
    end_date = forms.CharField(label="終了<br>月日", max_length=5, required=False,
                               widget=forms.Textarea(
                                   attrs={'cols': '6', 'rows': '1', 'class': 'td_menu'}))
    payment_slip_exist = forms.ChoiceField(label="納付書", choices=f.check, required=False,
                                           widget=forms.Select(attrs={'cols': '2', 'rows': '1', 'class': 'td_form'}))
    payment_slip_date = forms.CharField(label="納付書<br>月日", max_length=5, required=False,
                                        widget=forms.Textarea(
                                            attrs={'cols': '6', 'rows': '1', 'class': 'td_menu'}))
    report_create_date = forms.CharField(label="申告書<br>作成日", max_length=5, required=False,
                                         widget=forms.Textarea(
                                             attrs={'cols': '6', 'rows': '1', 'class': 'td_menu'}))
    fair_copy_date = forms.CharField(label="清書<br>終了日", max_length=5, required=False,
                                     widget=forms.Textarea(
                                         attrs={'cols': '6', 'rows': '1', 'class': 'td_menu'}))
    boss_stamp_date = forms.CharField(label="所長<br>捺印日", max_length=5, required=False,
                                      widget=forms.Textarea(
                                          attrs={'cols': '6', 'rows': '1', 'class': 'td_menu'}))
    client_stamp_date = forms.CharField(label="納税者<br>捺印日", max_length=5, required=False,
                                        widget=forms.Textarea(
                                            attrs={'cols': '6', 'rows': '1', 'class': 'td_menu'}))
    filing_date = forms.CharField(label="申告書<br>提出日", max_length=5, required=False,
                                  widget=forms.Textarea(
                                      attrs={'cols': '6', 'rows': '1', 'class': 'td_menu'}))

    reward_billing_amount = forms.IntegerField(label="報酬<br>請求額", max_value=10000000, required=False, initial=0,
                                               widget=forms.Textarea(
                                                   attrs={'cols': '6', 'rows': '1', 'class': 'td_int'}))
    reward_withholding = forms.IntegerField(label="報酬厳<br>選額", max_value=10000000, required=False, initial=0,
                                            widget=forms.Textarea(
                                                attrs={'cols': '6', 'rows': '1', 'class': 'td_int'}))
    copy1 = forms.ChoiceField(label="コピー", choices=f.check_circle, required=False,
                              widget=forms.Textarea(
                                  attrs={'cols': '6', 'rows': '1', 'class': 'td_menu'}))
    note = global_note_table


class InvoiceCreateForm(forms.Form):
    date = forms.DateField(label='日付', initial=datetime.date.today())
    number = global_number
    number_choice = global_number_choice
    content_choice = (
        ('税務顧問報酬', '税務顧問報酬'), ('会計顧問報酬', '会計顧問報酬'), ('税務代理報酬', '税務代理報酬'),
        ('税務書類作成報酬', '税務書類作成報酬'), ('税務相談報酬', '税務相談報酬'), ('調査立会報酬', '調査立会報酬'),
        ('決算書類作成報酬', '決算書類作成報酬'), ('消費税書類作成報酬', '消費税書類作成報酬'), ('年末調整量', '年末調整量'),
        ('償却資産申告書作成料', '償却資産申告書作成料'), ('その他', 'その他'),
    )
    content = forms.ChoiceField(label='内容', choices=content_choice)
    items = forms.CharField(label='内訳', max_length=100)
    money = forms.IntegerField(label='金額', max_value=90000000, required=False)
    consumption = forms.IntegerField(label='消費税', max_value=90000000, required=False)
    withholding_income_tax = forms.IntegerField(label='源泉所得税', max_value=90000000, required=False)
    reconstruction_tax = forms.IntegerField(label='特別復興税', max_value=90000000, required=False)

    transfer_date = forms.CharField(label="振替日<br>無い場合は空白", max_length=10, required=False,
                                    widget=forms.TextInput(attrs={'placeholder': '1月1日'}))


class ClientSearchForm(forms.Form):
    name = forms.CharField(label='顧問先名検索', max_length=200)


class InvolvedRosterForm(forms.Form):
    a = [('法人以外', '法人以外')]
    b = f.type_choices + a
    type = forms.ChoiceField(label='分類', choices=b)
    tax_agency = forms.ChoiceField(label='管轄税務署', choices=f.tax_agency)
    date = forms.DateField(label='日付', widget=forms.DateInput(attrs={"type": "date"}))


class WorkForm(forms.Form):
    year = global_year
    month = forms.IntegerField(label='月', max_value=12, min_value=1,
                             widget=forms.NumberInput(attrs={'placeholder': '1~12'}))
    day = forms.IntegerField(label='日', min_value=1, max_value=31,
                             widget=forms.NumberInput(attrs={'placeholder': '1~31'}))
    in_time = forms.CharField(label='出勤', max_length=5, widget=forms.TextInput(attrs={'placeholder': '0:00'}))
    out_time = forms.CharField(label='退勤', max_length=5, widget=forms.TextInput(attrs={'placeholder': '0:00'}))
    rest_time = forms.ChoiceField(label='休憩', choices=(('0:00', '0:00'), ('1:00', '1:00')))
    note = global_note
    distance = forms.FloatField(label='走行距離(km)', max_value=900, required=False)


class PrintRequestForm(forms.Form):
    number = global_number
    number_choice = global_number_choice
