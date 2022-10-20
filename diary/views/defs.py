import django.core.exceptions

from diary.models import ClientList
from django.db.models import CharField, Value
from django.db.models.functions import Concat
from django.utils.datastructures import MultiValueDictKeyError
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.db.models import Q, F
from private_diary.settings import PDF_DIR
import os
from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl
import datetime

def number_choice():  # 顧問先番号のChoiceFieldを生成する
    choice = list(ClientList.objects.select_related().values_list(
        'k_number', Concat('k_number', Value(' '), 'k_name', output_field=CharField())
    ).order_by('k_number'))
    choice.insert(0, ('', ''))
    return choice


def number_post(a, b):  # defs.number_post(self.POST['number'], self.POST['number_choice'])
    if a != '':
        number = a
    elif b != '':
        number = b
    else:
        number = 0
    return number


def key_to_blank(a, b):  # defs.key_to_blank(request.POST, 'var')
    try:
        c = a[b]
    except MultiValueDictKeyError:
        c = ''
    return c


def select_year_tax_agency_manager(model, year, tax_agency, manager):
    if tax_agency != '' and manager != '':
        p = model.objects.select_related().filter(
            Q(year=year), Q(tax_agency=tax_agency),
            Q(k_number__manager1=manager) | Q(k_number__manager2=manager)
        ).order_by('k_number_id')
    elif tax_agency != '':
        p = model.objects.select_related().filter(
            year=year, tax_agency=tax_agency).order_by('k_number_id')
    elif manager != '':
        p = model.objects.select_related().filter(
            Q(year=year),
            Q(k_number__manager1=manager) | Q(k_number__manager2=manager)
        ).order_by('k_number_id')
    else:
        p = model.objects.select_related().filter(
            year=year,
        ).order_by('k_number_id')

    return p


def select_year_month(model, year, month):
    p = model.objects.select_related().filter(
        year=year, month=month
    ).order_by(F('insert_date').asc(nulls_first=True), 'k_number_id')

    return p

def pdf_create(pdf_name: str, pdf_template: str or None, cv: canvas.Canvas, size: tuple,
               header_font: int, main_font: int, footer_font: int, list_name_font: int,
               header_list: tuple, main_list: tuple, main_list2: tuple, footer_list: tuple, list_name: tuple,
               x_list: tuple, y_list: list,
               list_height: int, list_rows: int):
    ttf_file = os.path.join(PDF_DIR + '/IPAexfont00401/ipaexg.ttf')
    pdfmetrics.registerFont(TTFont('IPAexGothic', ttf_file))
    cv.setTitle(pdf_name)
    h, w = size
    h, w = int(h), int(w)
    page_count = 1
    if pdf_template is not None:
        cv.doForm(makerl(cv, pagexobj(PdfReader(pdf_template, decompress=False).pages[0])))
    for i in range(list_rows + 1):
        y_list.append(y_list[0] - i * list_height)

    def other(font: int, lists: tuple):  # ヘッダーやフッターで使う
        cv.setFont('IPAexGothic', font)
        for li in lists:
            if li[0] == 0:
                cv.drawString(li[1], li[2], li[3])
            elif li[0] == 1:
                cv.drawCentredString(li[1], li[2], li[3])
            elif li[0] == 2:
                cv.drawRightString(li[1], li[2], li[3])

    other(header_font, header_list)
    other(footer_font, footer_list)
    cv.drawCentredString(w / 2, 20, str(page_count))
    other(list_name_font, list_name)
    # 本文
    cv.setFont('IPAexGothic', main_font)
    q = y_list[0]
    for i, ml in enumerate(main_list, start=1):
        for j, m in enumerate(ml, start=0):
            if m is not None:
                cv.drawString(x_list[j] + 2, q - i * list_height + 2, str(m))
            if len(main_list2) != 0:
                if main_list2[i - 1][j] is not None:
                    cv.drawString(x_list[j] + 2, q - i * list_height + 2 + 20, str(main_list2[i - 1][j]))
        if i % list_rows == 0:
            q += list_height * list_rows
            cv.grid(x_list, y_list)
            cv.showPage()
            if pdf_template is not None:
                cv.doForm(makerl(cv, pagexobj(PdfReader(pdf_template, decompress=False).pages[0])))
            other(header_font, header_list)
            other(footer_font, footer_list)
            page_count += 1
            cv.drawCentredString(w / 2, 20, str(page_count))
            other(list_name_font, list_name)

    cv.grid(x_list, y_list)
    cv.save()


accounting_date_list = [
    ("4月30日", "無", "無", ['2月28日']),
    ("4月30日", "無", "1回", ('2月28日', '8月31日')),
    ("4月30日", "無", "3回", ('2月28日', '5月30日', '8月31日', '11月30日')),
    ("4月30日", "有", "無", ['8月31日']),
    ("4月30日", "有", "1回", ('8月31日', '2月28日')),
    ("4月30日", "有", "3回", ('8月31日', '11月30日', '2月28日', '5月31日')),

    ("5月31日", "無", "無", ['3月31日']),
    ("5月31日", "無", "1回", ('3月31日', '9月30日')),
    ("5月31日", "無", "3回", ('3月31日', '6月30日', '9月30日', '12月31日')),
    ("5月31日", "有", "無", ['9月30日']),
    ("5月31日", "有", "1回", ('9月30日', '3月31日')),
    ("5月31日", "有", "3回", ('9月30日', '12月31日', '3月31日', '6月30日')),

    ("6月30日", "無", "無", ['4月30日']),
    ("6月30日", "無", "1回", ('4月30日', '10月31日')),
    ("6月30日", "無", "3回", ('4月30日', '7月31日', '10月31日', '1月31日')),
    ("6月30日", "有", "無", ['10月31日']),
    ("6月30日", "有", "1回", ('10月31日', '4月30日')),
    ("6月30日", "有", "3回", ('10月31日', '1月31日', '4月30日', '7月31日')),

    ("7月31日", "無", "無", ['5月31日']),
    ("7月31日", "無", "1回", ('5月31日', '11月30日')),
    ("7月31日", "無", "3回", ('5月31日', '8月31日', '11月30日', '2月28日')),
    ("7月31日", "有", "無", ['11月30日']),
    ("7月31日", "有", "1回", ('11月30日', '5月31日')),
    ("7月31日", "有", "3回", ('11月30日', '2月28日', '5月31日', '8月31日')),

    ("8月31日", "無", "無", ['6月30日']),
    ("8月31日", "無", "1回", ('6月30日', '12月31日')),
    ("8月31日", "無", "3回", ('6月30日', '9月30日', '12月31日', '3月31日')),
    ("8月31日", "有", "無", ['12月31']),
    ("8月31日", "有", "1回", ('12月31日', '6月30日')),
    ("8月31日", "有", "3回", ('12月31日', '3月31日', '6月30日', '9月30日')),

    ("9月30日", "無", "無", ['7月31日']),
    ("9月30日", "無", "1回", ('7月31日', '1月31日')),
    ("9月30日", "無", "3回", ('7月31日', '10月31日', '1月31日', '4月30日')),
    ("9月30日", "有", "無", ['1月31日']),
    ("9月30日", "有", "1回", ('1月31日', '7月31日')),
    ("9月30日", "有", "3回", ('1月31日', '4月30日', '7月31日', '10月31日')),

    ("10月31日", "無", "無", ['8月31日']),
    ("10月31日", "無", "1回", ('8月31日', '2月28日')),
    ("10月31日", "無", "3回", ('8月31日', '11月30日', '2月28日', '5月31日')),
    ("10月31日", "有", "無", ['2月28日']),
    ("10月31日", "有", "1回", ('2月28日', '8月31日')),
    ("10月31日", "有", "3回", ('2月28日', '5月31日', '8月31日', '11月30日')),

    ("11月30日", "無", "無", ['9月30日']),
    ("11月30日", "無", "1回", ('9月30日', '3月31日')),
    ("11月30日", "無", "3回", ('9月30日', '12月31日', '3月31日', '6月30日')),
    ("11月30日", "有", "無", ['3月31日']),
    ("11月30日", "有", "1回", ('3月31日', '9月30日')),
    ("11月30日", "有", "3回", ('3月31日', '6月30日', '9月30日', '12月31日')),

    ("12月31日", "無", "無", ['10月31日']),
    ("12月31日", "無", "1回", ('10月31日', '4月30日')),
    ("12月31日", "無", "3回", ('10月31日', '1月31日', '4月30日', '7月31日')),
    ("12月31日", "有", "無", ['4月30日']),
    ("12月31日", "有", "1回", ('4月30日', '10月30日')),
    ("12月31日", "有", "3回", ('4月30日', '7月31日', '10月30日', '1月31日')),

    ("1月31日", "無", "無", ['11月30日']),
    ("1月31日", "無", "1回", ('11月30日', '5月31日')),
    ("1月31日", "無", "3回", ('11月30日', '2月28日', '5月31日', '8月31日')),
    ("1月31日", "有", "無", ['5月31日']),
    ("1月31日", "有", "1回", ('5月31日', '11月30日')),
    ("1月31日", "有", "3回", ('5月31日', '8月31日', '11月30日', '2月28日')),

    ("2月28日", "無", "無", ['12月31日']),
    ("2月28日", "無", "1回", ('12月31日', '6月30日')),
    ("2月28日", "無", "3回", ('12月31日', '3月31日', '6月30日', '9月30日')),
    ("2月28日", "有", "無", ['6月30日']),
    ("2月28日", "有", "1回", ('6月30日', '12月31日')),
    ("2月28日", "有", "3回", ('6月30日', '9月30日', '12月31日', '3月31日')),

    ("3月31日", "無", "無", ['1月31日']),
    ("3月31日", "無", "1回", ('1月31日', '7月31日')),
    ("3月31日", "無", "3回", ('1月31日', '4月30日', '7月31日', '10月31日')),
    ("3月31日", "有", "無", ['7月31日']),
    ("3月31日", "有", "1回", ('7月31日', '1月31日')),
    ("3月31日", "有", "3回", ('7月31日', '10月31日', '1月31日', '4月30日')),

    ("3月20日", "無", "無", ['1月20日']),
    ("3月20日", "無", "1回", ('1月20日', '7月20日')),
    ("3月20日", "無", "3回", ('1月20日', '4月20日', '7月20日', '10月20日')),
    ("3月20日", "有", "無", ['7月20日']),
    ("3月20日", "有", "1回", ('7月20日', '1月20日')),
    ("3月20日", "有", "3回", ('7月20日', '10月20日', '1月20日', '4月20日')),

    ("5月20日", "無", "無", ['3月20日']),
    ("5月20日", "無", "1回", ('3月20日', '9月20日')),
    ("5月20日", "無", "3回", ('3月20日', '6月20日', '9月20日', '12月20日')),
    ("5月20日", "有", "無", ['9月20日']),
    ("5月20日", "有", "1回", ('9月20日', '3月20日')),
    ("5月20日", "有", "3回", ('9月20日', '12月20日', '3月20日', '6月20日')),
]
