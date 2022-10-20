import datetime
import math
import random
import re

from django.shortcuts import render
from django.views.generic import TemplateView
from japanera import EraDate
from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl
from reportlab.lib.pagesizes import A4, portrait, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from diary.forms import YearAdjustmentForm, YearManageTaxAgencyForm, YearNumberForm
from diary.forms import YearMonthForm, YearMonthNumberForm, FilingForm, FilingForm2, YearForm
from diary.forms import GiftTaxCheckForm, YearTaxAgencyTypeForm, WithholdingForm, FilingFinalTaxForm
from diary.models import YearAdjustment, ClientList, FilingFormList, GiftTax
from diary.models import WithholdingCheck, FilingFinalTax
from diary.views import defs
from private_diary.settings import PDF_DIR

class ViewsFilingFinalTax(TemplateView):
    template_name = "base_document.html"

    def get(self, request, **kwargs):  # title,form,create of a year
        params = {'title': "確定申告進行チェック表", 'read_form': YearManageTaxAgencyForm(),
                  'create_form': YearNumberForm(), 'year': datetime.date.today().year,
                  'reward_billing_amount': 0, 'withholding': 0}
        params['create_form'].fields['number_choice'].choices = defs.number_choice()
        if len(FilingFinalTax.objects.select_related().filter(year=params['year'])) == 0:
            lists = ClientList.objects.select_related().filter(contract_cancellation='無', type='個人')
            for lis in lists:
                FilingFinalTax(year=params['year'], k_number_id=lis.k_number,
                               report_category=lis.report_category, tax_agency=lis.tax_agency).save()
            params['check'] = str(params['year']) + "年のデータを出力しました!"
        return render(request, 'base_document.html', params)

    def post(self, request, **kwargs):
        params = {'form': None, 'year': datetime.date.today().year, 'manager': None, 'tax_agency': None}
        forms = []
        params['year'] = request.POST['year']
        params['manager'] = request.POST['manager']
        params['tax_agency'] = request.POST['tax_agency']
        if 'btn-c' in request.POST:
            params['number'] = defs.number_post(request.POST['number'], request.POST['number_choice'])
            try:
                FilingFinalTax.objects.get(year=params['year'], k_number_id=params['number'])
                params['check'] = "既に存在します。"
            except FilingFinalTax.DoesNotExist:
                try:
                    k = ClientList.objects.get(k_number=params['number'])
                    FilingFinalTax(year=params['year'], k_number_id=params['number'],
                                   report_category=k.report_category, tax_agency=k.tax_agency).save()
                    params['check'] = "追加しました!"
                except ClientList.DoesNotExist:
                    params['check'] = "名簿に存在しません。"
        elif 'btn-u' in request.POST:  # 変更
            params['number'] = request.POST['number']
            try:
                cu = FilingFinalTax.objects.get(year=params['year'], k_number_id=params['number'])
                cu.report_form_category = request.POST['report_form_category']
                cu.report_category = request.POST['report_category']
                cu.consumption_report = request.POST['consumption_report']
                cu.filing = request.POST['filing']
                cu.sales = defs.key_to_blank(request.POST, 'sales')
                cu.agriculture = defs.key_to_blank(request.POST, 'agriculture')
                cu.real_estate = defs.key_to_blank(request.POST, 'real_estate')
                cu.interest = defs.key_to_blank(request.POST, 'interest')
                cu.dividend = defs.key_to_blank(request.POST, 'dividend')
                cu.salary = defs.key_to_blank(request.POST, 'salary')
                cu.pension = defs.key_to_blank(request.POST, 'pension')
                cu.other = defs.key_to_blank(request.POST, 'other')
                cu.comprehensive = defs.key_to_blank(request.POST, 'comprehensive')
                cu.separation = defs.key_to_blank(request.POST, 'separation')
                cu.temporary = defs.key_to_blank(request.POST, 'temporary')
                cu.income_tax = request.POST['income_tax']
                cu.consumption = request.POST['consumption']
                cu.fair_copy_date = request.POST['fair_copy_date']
                cu.seal_check_date = request.POST['seal_check_date']
                cu.boss_stamp_date = request.POST['boss_stamp_date']
                cu.electronic_end_date = request.POST['electronic_end_date']
                cu.attached_document_filing_date = request.POST['attached_document_filing_date']
                cu.billing_amount = request.POST['billing_amount']
                cu.withholding = request.POST['withholding']
                cu.note = request.POST['note']
                cu.filing2 = request.POST['filing2']
                cu.save()
                params['check'] = "変更しました!"
            except FilingFinalTax.DoesNotExist:
                params['check'] = "存在しません。"
        elif 'btn-d' in request.POST:  # 削除
            params['number'] = request.POST['number']
            FilingFinalTax.objects.filter(year=params['year'], k_number_id=params['number']).delete()
            params['check'] = "削除しました！"
        elif 'btn-p' in request.POST:
            params['tax_agency'] = request.POST['tax_agency']
            params['manager'] = request.POST['manager']
            p = defs.select_year_tax_agency_manager(
                FilingFinalTax, params['year'], params['tax_agency'], params['manager'])
            ttf_file = './private_diary/diary/media/IPAexfont00401/ipaexg.ttf'
            pdfmetrics.registerFont(TTFont('IPAexGothic', ttf_file))
            w, h = portrait(A4)
            rnd = str(math.floor(random.random() * 100))
            cv = canvas.Canvas('private_diary/diary/media/確定申告PDF/' + rnd + '.pdf', pagesize=landscape(A4))
            font_size = 8
            cv.setFont('IPAexGothic', font_size)
            file_in = 'private_diary/diary/media/filing_final_tax_template.pdf'

            page = PdfReader(file_in, decompress=False).pages
            pp = pagexobj(page[0])
            cv.doForm(makerl(cv, pp))
            font_size = 8
            cv.setFont('IPAexGothic', font_size)
            page_count = 1
            t = w - 110
            for count, i in enumerate(p):
                cv.drawString(5, t, i.k_number.k_name)
                if i.report_form_category is not None:
                    cv.drawCentredString(80, t, i.report_form_category)
                if i.report_category is not None:
                    cv.drawCentredString(105, t, i.report_category)
                if i.consumption_report is not None:
                    cv.drawCentredString(135, t, i.consumption_report)
                if i.filing is not None:
                    cv.drawCentredString(160, t, i.filing)
                if i.sales is not None:
                    cv.drawCentredString(180, t, i.sales)
                if i.agriculture is not None:
                    cv.drawCentredString(200, t, i.agriculture)
                if i.real_estate is not None:
                    cv.drawCentredString(220, t, i.real_estate)
                if i.interest is not None:
                    cv.drawCentredString(240, t, i.interest)
                if i.dividend is not None:
                    cv.drawCentredString(260, t, i.dividend)
                if i.salary is not None:
                    cv.drawCentredString(280, t, i.salary)
                if i.pension is not None:
                    cv.drawCentredString(300, t, i.pension)
                if i.other is not None:
                    cv.drawCentredString(320, t, i.other)
                if i.comprehensive is not None:
                    cv.drawCentredString(340, t, i.comprehensive)
                if i.separation is not None:
                    cv.drawCentredString(360, t, i.separation)
                if i.temporary is not None:
                    cv.drawCentredString(380, t, i.temporary)
                if i.income_tax is not None:
                    cv.drawCentredString(405, t, i.income_tax)
                if i.consumption is not None:
                    cv.drawCentredString(435, t, i.consumption)
                if i.fair_copy_date is not None:
                    cv.drawCentredString(465, t, i.fair_copy_date)
                if i.seal_check_date is not None:
                    cv.drawCentredString(495, t, i.seal_check_date)
                if i.boss_stamp_date is not None:
                    cv.drawCentredString(525, t, i.boss_stamp_date)
                if i.electronic_end_date is not None:
                    cv.drawCentredString(555, t, i.electronic_end_date)
                if i.attached_document_filing_date is not None:
                    cv.drawCentredString(585, t, i.attached_document_filing_date)
                if i.billing_amount is not None:
                    cv.drawRightString(629, t, str(i.billing_amount))
                if i.withholding is not None:
                    cv.drawRightString(659, t, str(i.withholding))
                if i.note is not None:
                    cv.drawCentredString(675, t, i.note)
                if i.filing2 is not None:
                    gyo = i.filing2.count(',') + 1
                    s = re.split('[、+,]', i.filing2)
                    for gy in range(gyo):
                        cv.drawString(692, t, s[gy])
                        t -= 15
                # t -= 15
                if t <= w - 505 or count == 0:
                    if count != 0:
                        cv.showPage()
                        t = w - 110
                    font_size = 12
                    cv.setFont('IPAexGothic', font_size)
                    cv.drawCentredString(h / 2, 20, str(page_count))
                    page_count += 1
                    cv.drawString(250, w - 20, "令和　　年")
                    cv.drawRightString(298, w - 20, str(int(params['year']) - 2018))
                    cv.drawString(360, w - 20, "確定申告進行チェック表")
                    if params['tax_agency'] != '':
                        cv.drawString(10, w - 40, "税務署:")
                        cv.drawString(70, w - 40, params['tax_agency'])
                    else:
                        cv.drawString(10, w - 40, "担当者:")
                        cv.drawString(70, w - 40, params['manager'])
                    # 画像ファイルの挿入
                    font_size = 8
                    cv.setFont('IPAexGothic', font_size)
                    page = PdfReader(file_in, decompress=False).pages
                    pp = pagexobj(page[0])
                    cv.doForm(makerl(cv, pp))
            cv.save()
            params['check'] = rnd + '.pdfを出力しました!'
            url = str(request.META.get("HTTP_HOST"))
            params['file'] = 'http://' + url + '/diary/media/確定申告PDF/' + str(rnd) + '.pdf'
        rs = defs.select_year_tax_agency_manager(
            FilingFinalTax, params['year'], params['tax_agency'], params['manager'])
        billing_amount_sum = 0
        withholding_sum = 0
        for r in rs:
            initial_dict = dict(manager=params['manager'],
                                tax_agency=r.tax_agency,
                                number=r.k_number_id,
                                year=r.year,
                                k_name=r.k_number.k_name,
                                report_form_category=r.report_form_category,
                                report_category=r.report_category,
                                consumption_report=r.consumption_report,
                                filing=r.filing,
                                sales=r.sales,
                                agriculture=r.agriculture,
                                real_estate=r.real_estate,
                                interest=r.interest,
                                dividend=r.dividend,
                                salary=r.salary,
                                pension=r.pension,
                                other=r.other,
                                comprehensive=r.comprehensive,
                                separation=r.separation,
                                temporary=r.temporary,
                                income_tax=r.income_tax,
                                consumption=r.consumption,
                                fair_copy_date=r.fair_copy_date,
                                seal_check_date=r.seal_check_date,
                                boss_stamp_date=r.boss_stamp_date,
                                electronic_end_date=r.electronic_end_date,
                                attached_document_filing_date=r.attached_document_filing_date,
                                billing_amount=r.billing_amount,
                                withholding=r.withholding,
                                note=r.note,
                                filing2=r.filing2)
            billing_amount_sum += r.billing_amount
            withholding_sum += r.withholding
            forms.append(FilingFinalTaxForm(initial=initial_dict))
        params['table_title'] = "件数:" + str(rs.count()) + " 請求額:" + str(billing_amount_sum) + \
                                "円 源泉額:" + str(withholding_sum) + "円"
        params['table_form'] = forms
        params['read_form'] = YearManageTaxAgencyForm(request.POST)
        params['create_form'] = YearNumberForm(request.POST)
        params['create_form'].fields['number_choice'].choices = defs.number_choice()
        params['title'] = "確定申告進行チェック表"
        params['max_width'] = "1720px"
        return render(request, 'base_document.html', params)


class ViewsWithholding(TemplateView):
    template_name = "base_document.html"

    def get(self, request, **kwargs):  # title,form,create of a year
        params = {'title': "源泉税納期特例チェック表", 'read_form': YearTaxAgencyTypeForm(),
                  'create_form': YearNumberForm(), 'year': datetime.date.today().year,
                  'reward_billing_amount': 0, 'withholding': 0}
        params['create_form'].fields['number_choice'].choices = defs.number_choice()
        if len(WithholdingCheck.objects.select_related().filter(year=params['year'])) == 0:
            lists = ClientList.objects.filter(
                contract_cancellation='無', withholding_tax_method='納期特例').order_by('k_number')
            for lis in lists:
                WithholdingCheck(year=params['year'], k_number_id=lis.k_number,
                                 type=lis.type, tax_agency=lis.tax_agency).save()
            params['check'] = str(params['year']) + "年のデータを出力しました!"
        return render(request, 'base_document.html', params)

    def post(self, request, **kwargs):
        params = {'form': None, 'year': datetime.date.today().year, 'tax_agency': None, 'type': None}
        forms = []
        params['year'] = request.POST['year']
        params['tax_agency'] = request.POST['tax_agency']
        params['type'] = request.POST['type']
        if 'btn-c' in request.POST:
            params['number'] = defs.number_post(request.POST['number'], request.POST['number_choice'])
            try:
                WithholdingCheck.objects.get(year=params['year'],
                                             k_number_id=params['number'])
                params['check'] = "既に存在します。"
            except WithholdingCheck.DoesNotExist:
                try:
                    k = ClientList.objects.get(k_number=params['number'])
                    c = WithholdingCheck(year=params['year'],
                                         k_number_id=params['number'],
                                         type=k.type,
                                         tax_agency=k.tax_agency)
                    c.save()
                    params['check'] = "追加しました!"
                except ClientList.DoesNotExist:
                    params['check'] = "名簿に存在しません。"
        elif 'btn-u' in request.POST:  # 変更
            params['number'] = defs.number_post(request.POST['number'], request.POST['number_choice'])
            try:
                u = WithholdingCheck.objects.get(year=params['year'], k_number_id=params['number'])
                u.type = request.POST['type']
                u.tax_agency = request.POST['tax_agency']
                u.withholding_tax_method = request.POST['withholding_tax_method']
                u.delivery_date = request.POST['delivery_date']
                u.mail_date = request.POST['mail_date']
                u.note = request.POST['note']
                u.save()
                params['check'] = "変更しました!"
            except WithholdingCheck.DoesNotExist:
                params['check'] = "存在しません。"
        elif 'btn-d' in request.POST:  # 削除
            params['number'] = defs.number_post(request.POST['number'], request.POST['number_choice'])
            WithholdingCheck.objects.filter(year=params['year'], k_number_id=params['number']).delete()
            params['check'] = "削除しました！"
        elif 'btn-p' in request.POST:
            p = WithholdingCheck.objects.filter(year=params['year']).order_by('k_number_id')
            if len(p) == 0:
                params['check'] = "データベースに存在しません。"
            else:
                h, w = portrait(A4)
                h, w = int(h), int(w)
                rnd = str(math.floor(random.random() * 100))
                pdf_param = {'pdf_name': '贈与税申告進行チェック表',
                             'pdf_template': None,
                             'cv': canvas.Canvas(PDF_DIR + '/源泉税納期特例チェックPDF/' + rnd + '.pdf', pagesize=landscape(A4)),
                             'size': portrait(landscape(A4)),
                             'header_font': 12,
                             'main_font': 12,
                             'footer_font': 12,
                             'list_name_font': 12,
                             'header_list': (
                                 (1, 250, h - 30, EraDate(int(params['year']), 4, 1).strftime("%-E%-O年")),
                                 (1, 360, h - 50, "源泉税納期特例チェック表"),
                             ),
                             'list_name': (
                                 (5, w - 53, "番号"),
                                 (50, w - 53, "顧問先名"),
                                 (200, w - 53, "管轄税務署"),
                                 (280, w - 53, "源泉納付方法"),
                                 (360, w - 53, "納付書渡し"),
                                 (440, w - 53, "納付書郵送"),
                                 (520, w - 53, "備考"),
                             ),
                             'main_list': p.values_list('k_number_id',
                                                        'k_number__k_name',
                                                        'tax_agency',
                                                        'withholding_tax_method',
                                                        'delivery_date',
                                                        'mail_date'
                                                        ),
                             'main_list2': (),
                             'footer_list': (),
                             'x_list': (5, 50, 200, 280, 360, 440, 520, 590),
                             'y_list': [h - 55],
                             'list_height': 20,
                             'list_rows': 22,
                             }
                defs.pdf_create(**pdf_param)

                params['file'] = 'http://' + str(request.META.get("HTTP_HOST")) + \
                                 '/diary/media/源泉税納期特例チェックPDF/' + str(rnd) + '.pdf'
                params['check'] = "PDFを出力しました!"
        rs = WithholdingCheck.objects.select_related().filter(
            year=params['year'], tax_agency=params['tax_agency'], type=params['type']
        ).order_by('k_number_id')
        for i, r in enumerate(rs):
            initial_dict = dict(year=r.year,
                                number=r.k_number_id,
                                k_name=r.k_number.k_name,
                                type=r.type,
                                tax_agency=r.tax_agency,
                                withholding_tax_method=r.withholding_tax_method,
                                delivery_date=r.delivery_date,
                                mail_date=r.mail_date,
                                note=r.note)
            forms.append(WithholdingForm(initial=initial_dict))
        params['table_title'] = "件数:" + str(rs.count())
        params['table_form'] = forms
        params['read_form'] = YearTaxAgencyTypeForm(request.POST)
        params['create_form'] = YearNumberForm(request.POST)
        params['create_form'].fields['number_choice'].choices = defs.number_choice()
        params['title'] = "贈与税申告進行チェック表"
        params['max_width'] = "1000px"
        return render(request, 'base_document.html', params)


class ViewsGiftTaxCheck(TemplateView):
    template_name = "base_document.html"

    def get(self, request, **kwargs):  # title,form,create of a year
        params = {'title': "贈与税申告進行チェック表", 'read_form': YearForm(), 'create_form': YearNumberForm(),
                  'year': datetime.date.today().year, 'reward_billing_amount': 0, 'withholding': 0}
        params['create_form'].fields['number_choice'].choices = defs.number_choice()
        if len(GiftTax.objects.filter(year=params['year'])) == 0:
            for i in ClientList.objects.filter(contract_cancellation='無', type='贈与税').order_by('k_number'):
                GiftTax(year=params['year'], k_number_id=i.k_number).save()
            params['check'] = str(params['year']) + "年のデータを出力しました!"
        return render(request, 'base_document.html', params)

    def post(self, request, **kwargs):
        params = {'form': None, 'year': datetime.date.today().year}
        forms = []
        params['year'] = request.POST['year']
        if 'btn-c' in request.POST:  # 追加
            params['number'] = defs.number_post(request.POST['number'], request.POST['number_choice'])
            try:
                GiftTax.objects.get(year=params['year'], k_number_id=params['number'])
                params['check'] = "既に存在します。"
            except GiftTax.DoesNotExist:
                ClientList.objects.get(k_number=params['number'])
                GiftTax(year=params['year'], k_number_id=params['number']).save()
                params['check'] = "追加しました!"
            except ClientList.DoesNotExist:
                params['check'] = "関与先名簿に存在しません。"
        elif 'btn-u' in request.POST:  # 変更
            params['number'] = request.POST['number']
            if request.POST['reward_withholding'] == '':
                params['reward_withholding'] = 0
            else:
                params['reward_withholding'] = request.POST['reward_withholding']
            if request.POST['reward_billing_amount'] == '':
                params['reward_billing_amount'] = 0
            else:
                params['reward_billing_amount'] = request.POST['reward_billing_amount']
            try:
                u = GiftTax.objects.get(year=params['year'], k_number_id=params['number'])
                u.tax_agency = request.POST['tax_agency']
                u.return_date = request.POST['return_date']
                u.end_date = request.POST['end_date']
                u.payment_slip_exist = request.POST['payment_slip_exist']
                u.payment_slip_date = request.POST['payment_slip_date']
                u.report_create_date = request.POST['report_create_date']
                u.fair_copy_date = request.POST['fair_copy_date']
                u.boss_stamp_date = request.POST['boss_stamp_date']
                u.client_stamp_date = request.POST['client_stamp_date']
                u.filing_date = request.POST['filing_date']
                u.electronic_or_paper = request.POST['electronic_or_paper']
                u.reward_billing_amount = params['reward_billing_amount']
                u.reward_withholding = params['reward_withholding']
                u.copy1 = request.POST['copy1']
                u.note = request.POST['note']
                u.save()
                params['check'] = "変更しました!"
            except GiftTax.DoesNotExist:
                params['check'] = "存在しません。"
        elif 'btn-d' in request.POST:
            GiftTax.objects.filter(year=params['year'], k_number_id=request.POST['number']).delete()
            params['check'] = "削除しました!"
        elif 'btn-p' in request.POST:
            p = GiftTax.objects.filter(year=params['year']).order_by('k_number_id')
            if len(p) == 0:
                params['check'] = "データベースに存在しません。"
            else:
                h, w = portrait(A4)
                h, w = int(h), int(w)
                rnd = str(math.floor(random.random() * 100))
                pdf_param = {'pdf_name': '贈与税申告進行チェック表',
                             'pdf_template': None,
                             'cv': canvas.Canvas(PDF_DIR + '/贈与税PDF/' + rnd + '.pdf', pagesize=landscape(A4)),
                             'size': portrait(A4),
                             'header_font': 12,
                             'main_font': 12,
                             'footer_font': 12,
                             'list_name_font': 12,
                             'header_list': (
                                 (1, 250, h - 30, EraDate(int(params['year']), 4, 1).strftime("%-E%-O年")),
                                 (1, 360, h - 50, "贈与税申告進行チェック表"),
                             ),
                             'list_name': (
                                 (0, 175, h - 95, "返却"),
                                 (0, 215, h - 95, "終了"),
                                 (0, 255, h - 95, ""),
                                 (1, 280, h - 95, "納付書"),
                                 (0, 315, h - 95, "申告書"),
                                 (0, 355, h - 95, "清書"),
                                 (0, 395, h - 95, "所長"),
                                 (0, 435, h - 95, "納税者"),
                                 (0, 490, h - 95, "申告書"),
                                 (0, 590, h - 95, "報酬"),
                                 (0, 705, h - 95, "備考"),
                                 (0, 175, h - 95, "返却"),
                                 (0, 21, h - 110, "提出税務署"),
                                 (0, 82, h - 110, "納税者名"),
                                 (0, 175, h - 110, "月日"),
                                 (0, 215, h - 110, "月日"),
                                 (1, 280, h - 110, "日付"),
                                 (0, 315, h - 110, "終了日"),
                                 (0, 355, h - 110, "終了日"),
                                 (0, 395, h - 110, "捺印日"),
                                 (0, 435, h - 110, "捺印日"),
                                 (0, 490, h - 110, "提出日"),
                                 (0, 555, h - 110, "請求額"),
                                 (0, 615, h - 110, "厳選額"),
                                 (1, 690, h - 90, "コ"),
                                 (1, 690, h - 100, "ピ"),
                                 (1, 688, h - 110, "  |"),
                             ),
                             'main_list': p.values_list('tax_agency',
                                                        'k_number__k_name',
                                                        'return_date',
                                                        'end_date',
                                                        'payment_slip_exist',
                                                        'payment_slip_date',
                                                        'report_create_date',
                                                        'fair_copy_date',
                                                        'boss_stamp_date',
                                                        'client_stamp_date',
                                                        'filing_date',
                                                        'electronic_or_paper',
                                                        'reward_billing_amount',
                                                        'reward_withholding',
                                                        'copy1',
                                                        'note'
                                                        ),
                             'main_list2': (),
                             'footer_list': (
                                 (2, 770, 15, '税理士業務処理簿(法第41条及び第48条の16)'),
                             ),
                             'x_list': (20, 80, 170, 210, 250, 270, 310, 350, 390, 430,
                                        470, 510, 550, 610, 680, 700, 820),
                             'y_list': [h - 112],
                             'list_height': 20,
                             'list_rows': 22,
                             }
                defs.pdf_create(**pdf_param)

                params['file'] = 'http://' + str(request.META.get("HTTP_HOST")) + \
                                 '/diary/media/贈与税PDF/' + str(rnd) + '.pdf'
                params['check'] = "PDFを出力しました!"
        rs = GiftTax.objects.filter(year=params['year']).order_by('k_number_id')
        reward_billing_amount_sum = 0
        withholding_sum = 0
        for i, r in enumerate(rs):
            initial_dict = dict(year=r.year,
                                number=r.k_number_id,
                                k_name=r.k_number.k_name,
                                tax_agency=r.tax_agency,
                                return_date=r.return_date,
                                end_date=r.end_date,
                                payment_slip_exist=r.payment_slip_exist,
                                payment_slip_date=r.payment_slip_date,
                                report_create_date=r.report_create_date,
                                fair_copy_date=r.fair_copy_date,
                                boss_stamp_date=r.boss_stamp_date,
                                client_stamp_date=r.client_stamp_date,
                                filing_date=r.filing_date,
                                electronic_or_paper=r.electronic_or_paper,
                                reward_billing_amount=r.reward_billing_amount,
                                reward_withholding=r.reward_withholding,
                                copy1=r.copy1,
                                note=r.note)
            reward_billing_amount_sum += r.reward_billing_amount
            withholding_sum += r.reward_withholding
            forms.append(GiftTaxCheckForm(initial=initial_dict))
        params['table_title'] = "件数:" + str(rs.count()) + \
                                " 請求額:" + str(reward_billing_amount_sum) + \
                                "円 源泉額:" + str(withholding_sum) + "円"
        params['table_form'] = forms
        params['read_form'] = YearForm(request.POST)
        params['create_form'] = YearNumberForm(request.POST)
        params['create_form'].fields['number_choice'].choices = defs.number_choice()
        params['title'] = "贈与税申告進行チェック表"
        params['max_width'] = "1450px"
        return render(request, 'base_document.html', params)


class ViewsYearAdjustment(TemplateView):
    template_name = "base_document.html"

    def get(self, request, **kwargs):  # title,form,create of a year
        params = {'title': "年末調整", 'read_form': YearManageTaxAgencyForm(), 'create_form': YearNumberForm(),
                  'year': datetime.date.today().year}
        params['create_form'].fields['number_choice'].choices = defs.number_choice()
        if len(YearAdjustment.objects.select_related().filter(year=params['year'])) == 0:
            lists = ClientList.objects.filter(contract_cancellation='無', year_adjustment_check='有')
            for l in lists:
                YearAdjustment(year=params['year'], k_number_id=l.k_number, tax_agency=l.tax_agency).save()
            params['check'] = str(params['year']) + "年のデータを出力しました!"
        return render(request, 'base_document.html', params)

    def post(self, request, **kwargs):
        params = {'form': None, 'year': datetime.date.today().year, 'tax_agency': None, 'manager': None}
        forms = []
        params['year'] = request.POST['year']
        if 'btn-c' in request.POST:  # 追加
            params['number'] = defs.number_post(request.POST['number'], request.POST['number_choice'])
            try:
                YearAdjustment.objects.get(year=params['year'], k_number_id=params['number'])
                params['check'] = "既に存在します。"
            except YearAdjustment.DoesNotExist:
                k = ClientList.objects.get(k_number=params['number'])
                YearAdjustment(year=params['year'], k_number_id=params['number'], tax_agency=k.tax_agency).save()
                params['check'] = "追加しました!"
            except ClientList.DoesNotExist:
                params['check'] = "関与先名簿に存在しません。"
        elif 'btn-u' in request.POST:  # 変更
            try:
                u = YearAdjustment.objects.get(year=params['year'], k_number_id=request.POST['number'])
                u.year_adjustment_day = request.POST['year_adjustment_day']
                u.personnel = request.POST['personnel']
                u.city_paper = request.POST['city_paper']
                u.city_electronic = request.POST['city_electronic']
                u.star = request.POST['star']
                u.payment_create_date = request.POST['payment_create_date']
                u.date = request.POST['date']
                u.payment_slip_delivery = request.POST['payment_slip_delivery']
                u.payment_slip_mail = request.POST['payment_slip_mail']
                u.billing_amount = request.POST['billing_amount']
                u.withholding_tax = request.POST['withholding_tax']
                u.invoice_number = request.POST['invoice_number']
                u.report_create_date = request.POST['report_create_date']
                u.filing_date = request.POST['filing_date']
                u.electronic_or_paper = request.POST['electronic_or_paper']
                u.billing_amount2 = request.POST['billing_amount2']
                u.withholding_tax2 = request.POST['withholding_tax2']
                u.note = request.POST['note']
                u.save()
                params['check'] = "変更しました!"
            except YearAdjustment.DoesNotExist:
                params['check'] = "存在しません。"
        elif 'btn-d' in request.POST:
            YearAdjustment.objects.filter(year=params['year'], k_number_id=request.POST['number']).delete()
            params['check'] = "削除しました!"
        elif 'btn-p' in request.POST:
            params['tax_agency'] = request.POST['tax_agency']
            params['manager'] = request.POST['manager']
            p = defs.select_year_tax_agency_manager(YearAdjustment, params['year'], params['tax_agency'],
                                                    params['manager'])
            if len(p) == 0:
                params['check'] = "データベースに存在しません。"
            else:
                h, w = portrait(A4)
                h, w = int(h), int(w)
                rnd = str(math.floor(random.random() * 100))
                pdf_param = {'pdf_name': '年末調整',
                             'pdf_template': None,
                             'cv': canvas.Canvas(PDF_DIR + '/年末調整PDF/' + rnd + '.pdf', pagesize=landscape(A4)),
                             'size': portrait(A4),
                             'header_font': 12,
                             'main_font': 8,
                             'footer_font': 8,
                             'list_name_font': 8,
                             'header_list': (
                                 (0, 60, h - 50, params['tax_agency']),
                                 (1, 250, h - 30, EraDate(int(params['year']), 4, 1).strftime("%-E%-O年")),
                                 (1, 360, h - 50, "年 末 調 整"),
                             ),
                             'list_name': (
                                 (0, 220, h - 88, "年末"),
                                 (0, 280, h - 88, "提出市町村数"),
                                 (0, 355, h - 88, "支払合計"),
                                 (0, 390, h - 88, "提出"),
                                 (0, 415, h - 88, "納付書"),
                                 (0, 445, h - 88, "納付書"),
                                 (0, 475, h - 88, "請求額"),
                                 (0, 570, h - 88, "申告書"),
                                 (0, 600, h - 88, "提出"),
                                 (0, 660, h - 88, "請求額"),
                                 (0, 5, h - 98, "番号"),
                                 (0, 30, h - 98, "顧問先名"),
                                 (0, 220, h - 98, "調整日"),
                                 (0, 250, h - 98, "調整人員"),
                                 (0, 280, h - 98, "(紙)"),
                                 (0, 310, h - 98, "(電子)"),
                                 (0, 355, h - 98, "表作成日"),
                                 (0, 387, h - 98, "完了日"),
                                 (0, 415, h - 98, "渡し"),
                                 (0, 445, h - 98, "郵送"),
                                 (0, 473, h - 98, "(税抜)"),
                                 (0, 505, h - 98, "源泉税"),
                                 (0, 535, h - 98, "請求書No"),
                                 (0, 570, h - 98, "作成日"),
                                 (0, 600, h - 98, "完了日"),
                                 (0, 630, h - 98, "源泉税"),
                                 (0, 660, h - 98, "(税抜)"),
                                 (0, 690, h - 98, "備考"),

                             ),
                             'main_list': p.values_list('k_number_id',
                                                        'k_number__k_name',
                                                        'personnel',
                                                        'city_paper',
                                                        'city_electronic',
                                                        'star',
                                                        'payment_create_date',
                                                        'date',
                                                        'payment_slip_delivery',
                                                        'payment_slip_mail',
                                                        'billing_amount',
                                                        'withholding_tax',
                                                        'invoice_number',
                                                        'report_create_date',
                                                        'filing_date',
                                                        'electronic_or_paper',
                                                        'billing_amount2',
                                                        'note',
                                                        ),
                             'main_list2': (),
                             'footer_list': (),
                             'x_list': (5, 30, 220, 250, 280, 310, 340, 355, 385, 415, 445,
                                        475, 505, 535, 570, 600, 630, 660, 690, 830),
                             'y_list': [h - 100],
                             'list_height': 20,
                             'list_rows': 20,
                             }
                defs.pdf_create(**pdf_param)

                params['file'] = 'http://' + str(request.META.get("HTTP_HOST")) + \
                                 '/diary/media/年末調整PDF/' + str(rnd) + '.pdf'
                params['check'] = "PDFを出力しました!"
        params['tax_agency'] = request.POST['tax_agency']
        params['manager'] = request.POST['manager']
        rs = defs.select_year_tax_agency_manager(YearAdjustment, params['year'], params['tax_agency'],
                                                 params['manager'])
        for i, r in enumerate(rs):
            initial_dict = dict(year=r.year,
                                number=r.k_number_id,
                                k_name=r.k_number.k_name,
                                tax_agency=r.tax_agency,
                                year_adjustment_day=r.year_adjustment_day,
                                personnel=r.personnel,
                                city_paper=r.city_paper,
                                city_electronic=r.city_electronic,
                                star=r.star,
                                payment_create_date=r.payment_create_date,
                                date=r.date,
                                payment_slip_delivery=r.payment_slip_delivery,
                                payment_slip_mail=r.payment_slip_mail,
                                billing_amount=r.billing_amount,
                                withholding_tax=r.withholding_tax,
                                invoice_number=r.invoice_number,
                                report_create_date=r.report_create_date,
                                filing_date=r.filing_date,
                                electronic_or_paper=r.electronic_or_paper,
                                billing_amount2=r.billing_amount2,
                                withholding_tax2=r.withholding_tax2,
                                note=r.note)
            forms.append(YearAdjustmentForm(initial=initial_dict))
        params['table_title'] = "件数:" + str(rs.count())
        params['table_form'] = forms
        params['read_form'] = YearManageTaxAgencyForm(request.POST)
        params['create_form'] = YearNumberForm(request.POST)
        params['create_form'].fields['number_choice'].choices = defs.number_choice()
        params['title'] = "年末調整"
        params['max_width'] = "1450px"
        return render(request, 'base_document.html', params)


class ViewsFiling(TemplateView):
    template_name = "base_document.html"

    def get(self, request, **kwargs):  # title,form,create of a year
        params = {'title': "提出一覧", 'read_form': YearMonthForm(), 'create_form': YearMonthNumberForm(),
                  'year': datetime.date.today().year}
        params['create_form'].fields['number_choice'].choices = defs.number_choice()
        accounting_date_list = defs.accounting_date_list
        if FilingFormList.objects.filter(year=params['year']).count() == 0:
            clients = ClientList.objects.select_related().filter(type='法人', contract_cancellation='無')
            for client in clients:
                # 消費税予定回数が11回の顧問先は例外処理をする
                if client.consumption_tax_times == '11回':
                    for i in ['1月31日', '2月28日', '3月31日', '4月30日', '5月31日', '6月30日',
                              '7月31日', '8月31日', '9月30日', '10月31日', '11月30日', '12月31日']:
                        FilingFormList(year=params['year'], month=i,
                                       k_number_id=client.k_number,
                                       accounting_date=client.accounting_date,
                                       consumption_tax_category=client.consumption_tax_category,
                                       consumption_tax_times=client.consumption_tax_times,
                                       tax_agency=client.tax_agency,
                                       regional_tax_office=client.regional_tax_office,
                                       government_office=client.government_office,
                                       report_schedule=client.report_schedule,
                                       ).save()
                for k_list in accounting_date_list:
                    check = 0
                    k = ''
                    if client.report_schedule == k_list[1]:
                        check += 1
                    if client.consumption_tax_times == k_list[2]:
                        check += 1
                    for accounting_date in k_list[3]:
                        if client.accounting_date == accounting_date:
                            check += 1
                            k = accounting_date
                    if check == 3:
                        FilingFormList(year=params['year'], month=k_list[0],
                                       k_number_id=client.k_number,
                                       accounting_date=k,
                                       consumption_tax_category=client.consumption_tax_category,
                                       consumption_tax_times=client.consumption_tax_times,
                                       tax_agency=client.tax_agency,
                                       regional_tax_office=client.regional_tax_office,
                                       government_office=client.government_office,
                                       report_schedule=client.report_schedule
                                       ).save()
            params['check'] = str(params['year']) + "年のデータを出力しました!"
        return render(request, 'base_document.html', params)

    def post(self, request, **kwargs):
        params = {'form': None, 'year': datetime.date.today().year, 'month': None, 'tax_agency': None, 'manager': None}
        forms = []
        params['year'] = request.POST['year']
        params['month'] = request.POST['month']
        if 'btn-c' in request.POST:  # 追加
            params['number'] = defs.number_post(request.POST['number'], request.POST['number_choice'])
            try:
                FilingFormList.objects.get(year=params['year'], month=params['month'],
                                           k_number_id=params['number'])
                params['check'] = "既に存在します。"
            except FilingFormList.DoesNotExist:
                k = ClientList.objects.get(k_number=params['number'])
                FilingFormList(year=params['year'], month=params['month'],
                               k_number_id=params['number'],
                               tax_agency=k.tax_agency, regional_tax_office=k.regional_tax_office,
                               government_office=k.government_office,
                               accounting_date=k.accounting_date,
                               consumption_tax_category=k.consumption_tax_category,
                               consumption_tax_times=k.consumption_tax_times
                               ).save()
                params['check'] = "追加しました!"
            except ClientList.DoesNotExist:
                params['check'] = "関与先名簿に存在しません。"
        elif 'btn-u' in request.POST:  # 変更
            try:
                u = FilingFormList.objects.get(year=params['year'], month=params['month'],
                                               k_number_id=request.POST['number'])
                u.tax_agency = request.POST['tax_agency']
                u.regional_tax_office = request.POST['regional_tax_office']
                u.government_office = request.POST['government_office']
                u.accounting_date = request.POST['accounting_date']
                u.consumption_tax_category = request.POST['consumption_tax_category']
                u.consumption_tax_times = request.POST['consumption_tax_times']
                u.report_schedule = request.POST['report_schedule']
                u.document1 = request.POST['document1']
                u.document2 = request.POST['document2']
                u.tax_agency_note = request.POST['tax_agency_note']
                u.regional_tax_office_note = request.POST['regional_tax_office_note']
                u.government_office_note = request.POST['government_office_note']
                u.report_schedule_note = request.POST['report_schedule_note']
                u.consumption_tax_times_note = request.POST['consumption_tax_times_note']
                if request.POST['insert_date'] == '':
                    u.insert_date = None
                else:
                    u.insert_date = request.POST['insert_date']
                u.insert_date_note = request.POST['insert_date_note']
                u.save()
                params['check'] = "変更しました!"
            except FilingFormList.DoesNotExist:
                params['check'] = "存在しません。"
        elif 'btn-d' in request.POST:
            FilingFormList.objects.filter(year=params['year'], month=params['month'],
                                          k_number_id=request.POST['number']).delete()
            params['check'] = "削除しました!"
        elif 'btn-p' in request.POST:
            p = defs.select_year_month(FilingFormList, params['year'], params['month'])
            if len(p) == 0:
                params['check'] = "データベースに存在しません。"
            else:
                h, w = portrait(A4)
                h, w = int(h), int(w)
                rnd = str(math.floor(random.random() * 100))
                pdf_param = {'pdf_name': str(params['year']) + params['month'] + '提出',
                             'pdf_template': None,
                             'cv': canvas.Canvas(PDF_DIR + '/提出一覧PDF/' + rnd + '.pdf', pagesize=landscape(A4)),
                             'size': portrait(A4),
                             'header_font': 12,
                             'main_font': 12,
                             'footer_font': 12,
                             'list_name_font': 12,
                             'header_list': ((1, w / 2, h - 20, params['month'] + "提出"),
                                             ),
                             'list_name': (
                                 # 20, 220, 330, 420, 570, 670, 710, 745, 820
                                 (0, 20, h - 70, '顧問先名'),
                                 (0, 20, h - 85, '決算期,区分'),
                                 (0, 220, h - 70, '申告等書類'),
                                 (0, 220, h - 85, '提出書類'),
                                 (0, 330, h - 70, '管轄税務署'),
                                 (0, 330, h - 85, '納付書:税務署'),
                                 (0, 420, h - 85, '県税事務所'),
                                 (0, 570, h - 85, '市町村役場'),
                                 (0, 670, h - 70, '予定'),
                                 (0, 670, h - 85, '申告'),
                                 (0, 710, h - 55, '消費税'),
                                 (0, 710, h - 70, '予定'),
                                 (0, 710, h - 85, '回数'),
                                 (0, 745, h - 85, '送信日'),
                             ),
                             'main_list2': p.values_list('k_number__k_name',
                                                         'document1',
                                                         'tax_agency',
                                                         'regional_tax_office',
                                                         'government_office',
                                                         'report_schedule',
                                                         'consumption_tax_times',
                                                         'insert_date',
                                                         ),
                             'main_list': p.values_list('accounting_date_consumption_tax_category',
                                                        'document2',
                                                        'tax_agency_note',
                                                        'regional_tax_office_note',
                                                        'government_office_note',
                                                        'report_schedule_note',
                                                        'consumption_tax_times_note',
                                                        'insert_date_note',
                                                        ),
                             'footer_list': (),
                             'x_list': (20, 220, 330, 420, 570, 670, 710, 745, 820,),
                             'y_list': [h - 92],
                             'list_height': 40,
                             'list_rows': 10,
                             }
                defs.pdf_create(**pdf_param)

                params['file'] = 'http://' + str(request.META.get("HTTP_HOST")) + \
                                 '/diary/media/提出一覧PDF/' + str(rnd) + '.pdf'
                params['check'] = "PDFを出力しました!"
        rs = defs.select_year_month(FilingFormList, params['year'], params['month'])
        for i, r in enumerate(rs):
            initial_dict = dict(year=r.year,
                                month=r.month,
                                number=r.k_number_id,
                                k_name=r.k_number.k_name,
                                tax_agency=r.tax_agency,
                                regional_tax_office=r.regional_tax_office,
                                government_office=r.government_office,
                                consumption_tax_times=r.consumption_tax_times,
                                report_schedule=r.report_schedule,
                                document1=r.document1,
                                insert_date=r.insert_date,
                                )
            forms.append(FilingForm(initial=initial_dict))

            initial_dict = dict(
                accounting_date=r.accounting_date,
                consumption_tax_category=r.consumption_tax_category,
                document2=r.document2,
                tax_agency_note=r.tax_agency_note,
                regional_tax_office_note=r.regional_tax_office_note,
                government_office_note=r.government_office_note,
                consumption_tax_times_note=r.consumption_tax_times_note,
                report_schedule_note=r.report_schedule_note,
                insert_date_note=r.insert_date_note,
            )
            forms.append(FilingForm2(initial=initial_dict))
        params['table_title'] = "件数:" + str(rs.count()) + " 送信件数:" + \
                                str(rs.exclude(insert_date=None).count())
        params['table_form'] = forms
        params['table_form_height'] = 2
        params['read_form'] = YearMonthForm(request.POST)
        params['create_form'] = YearMonthNumberForm(request.POST)
        params['create_form'].fields['number_choice'].choices = defs.number_choice()
        params['title'] = "提出一覧"
        params['max_width'] = "1200px"
        return render(request, 'base_document.html', params)
