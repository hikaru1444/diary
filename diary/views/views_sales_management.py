import datetime
import math
import random

from django.shortcuts import render
from reportlab.lib.pagesizes import A4, portrait, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from diary.forms import SalesManagementForm
from diary.models import SalesManagement, ClientList
from diary.views import defs


def views_sales_management(request):
    params = {'form': None, 'year': datetime.date.today().year}
    if request.method == 'POST':
        form = SalesManagementForm(request.POST)
        forms = []
        params['year'] = request.POST['year']
        if 'btn-c' in request.POST:  # 追加
            form = SalesManagementForm(request.POST)
            params['number'] = defs.number_post(request.POST['number'], request.POST['number_choice'])
            try:
                SalesManagement.objects.get(year=params['year'], k_number_id=params['number'])
                params['check'] = "既に存在します。"
            except SalesManagement.DoesNotExist:
                SalesManagement(year=params['year'], k_number_id=params['number']).save()
                params['check'] = "追加しました!"
        elif 'btn-d' in request.POST:
            params['bank'] = request.POST['bank']
            params['number'] = request.POST['number']
            SalesManagement.objects.filter(year=params['year'], k_number_id=params['number']).delete()
            params['check'] = "削除しました!"
        elif 'btn-u' in request.POST:
            params['bank'] = request.POST['bank']
            params['number'] = request.POST['number']
            try:
                u = SalesManagement.objects.get(year=params['year'], k_number_id=params['number'])
                u.m1 = request.POST['m1'] if request.POST['m1'] != '' else 0
                u.m2 = request.POST['m2'] if request.POST['m2'] != '' else 0
                u.m3 = request.POST['m3'] if request.POST['m3'] != '' else 0
                u.m4 = request.POST['m4'] if request.POST['m4'] != '' else 0
                u.m5 = request.POST['m5'] if request.POST['m5'] != '' else 0
                u.m6 = request.POST['m6'] if request.POST['m6'] != '' else 0
                u.m7 = request.POST['m7'] if request.POST['m7'] != '' else 0
                u.m8 = request.POST['m8'] if request.POST['m8'] != '' else 0
                u.m9 = request.POST['m9'] if request.POST['m9'] != '' else 0
                u.m10 = request.POST['m10'] if request.POST['m10'] != '' else 0
                u.m11 = request.POST['m11'] if request.POST['m11'] != '' else 0
                u.m12 = request.POST['m12'] if request.POST['m12'] != '' else 0
                u.first_tarm = request.POST['first_tarm'] if request.POST['first_tarm'] != '' else 0
                u.current_term = request.POST['current_term'] if request.POST['current_term'] != '' else 0
                u.save()
                params['check'] = "変更しました!"
            except SalesManagement.DoesNotExist:
                params['check'] = "存在しません。"
        elif 'btn-p' in request.POST:  # PDFを出力
            params['bank'] = request.POST['bank']
            ttf_file = './private_diary/diary/media/IPAexfont00401/ipaexg.ttf'
            pdfmetrics.registerFont(TTFont('IPAexGothic', ttf_file))
            w, h = portrait(A4)
            rnd = str(math.floor(random.random() * 100))
            # landscape(A4)を付けていると横向き
            cv = canvas.Canvas('./private_diary/diary/media/売上管理表PDF/' + rnd + '.pdf', pagesize=landscape(A4))
            font_size = 12
            cv.setFont('IPAexGothic', font_size)
            if request.POST['sales_withhold'] == '売上':
                p = SalesManagement.objects.select_related().filter(
                    year=params['year'], k_number__sales_management=params['bank'])
            else:
                pass

            # 線を引く
            xlist = (5, 150, 190, 230, 270, 310, 350, 390, 430, 470, 510, 550, 590, 630, 670, 710, 750, 790, 830)

            ylist = (w - 40, w - 55, w - 70, w - 85, w - 100, w - 115, w - 130, w - 145, w - 160,
                     w - 175, w - 190, w - 205, w - 220, w - 235, w - 250, w - 265, w - 280,
                     w - 295, w - 310, w - 325, w - 340, w - 355, w - 370, w - 385, w - 400,
                     w - 415, w - 430, w - 445, w - 460, w - 475, w - 490, w - 505)

            hearder = ["1月", "2月", "3月", "4月", "5月", "6月", "小計", "7月", "8月", "9月",
                       "10月", "11月", "12月", "小計", "前期未収", "当期未収", "合計"]
            page_count = 1
            sogokei = 0
            font_size = 8
            cv.setFont('IPAexGothic', font_size)
            # メイン部分
            t = w - 55
            syokei1 = 0
            syokei2 = 0
            for count, i in enumerate(p):
                cv.drawString(7, t, i.k_number.k_name)
                # 前期当期未収
                if i.first_tarm is not None:
                    cv.drawRightString(750, t, str(i.first_tarm))
                if i.current_term is not None:
                    cv.drawRightString(790, t, str(i.current_term))
                if i.m1 is not None:
                    cv.drawRightString(190, t, str(i.m1))
                    syokei1 += i.m1
                if i.m2 is not None:
                    cv.drawRightString(230, t, str(i.m2))
                    syokei1 += i.m2
                if i.m3 is not None:
                    cv.drawRightString(270, t, str(i.m3))
                    syokei1 += i.m3
                if i.m4 is not None:
                    cv.drawRightString(310, t, str(i.m4))
                    syokei1 += i.m4
                if i.m5 is not None:
                    cv.drawRightString(350, t, str(i.m5))
                    syokei1 += i.m5
                if i.m6 is not None:
                    cv.drawRightString(390, t, str(i.m6))
                    syokei1 += i.m6
                if i.m7 is not None:
                    cv.drawRightString(470, t, str(i.m7))
                    syokei2 += i.m7
                if i.m8 is not None:
                    cv.drawRightString(510, t, str(i.m8))
                    syokei2 += i.m8
                if i.m9 is not None:
                    cv.drawRightString(550, t, str(i.m9))
                    syokei2 += i.m9
                if i.m10 is not None:
                    cv.drawRightString(590, t, str(i.m10))
                    syokei2 += i.m10
                if i.m11 is not None:
                    cv.drawRightString(630, t, str(i.m11))
                    syokei2 += i.m11
                if i.m12 is not None:
                    cv.drawRightString(670, t, str(i.m12))
                    syokei2 += i.m12
                # 合計を書く
                cv.drawRightString(430, t, str(syokei1))
                cv.drawRightString(710, t, str(syokei2))
                cv.drawRightString(830, t, str(syokei1 + syokei2))
                syokei1 = 0
                syokei2 = 0
                t -= 15
                if count == 0 or count % 35 == 0:
                    if count != 0:
                        t = w - 55
                        cv.showPage()
                        page_count += 1
                    cv.drawString(h / 2, 20, str(page_count))
                    font_size = 12
                    cv.setFont('IPAexGothic', font_size)
                    cv.grid(xlist, ylist)
                    cv.drawString(250, w - 20, "令和　　年")
                    cv.drawRightString(298, w - 20, str(int(params['year']) - 2018))
                    cv.drawString(360, w - 20, "売上管理表")
                    cv.drawString(450, w - 20, params['bank'])
                    font_size = 8
                    cv.setFont('IPAexGothic', font_size)
                    # 列名を書く
                    for count, i in enumerate(hearder):
                        cv.drawRightString(190 + count * 40, w - 40, i)
            cv.save()
            params['check'] = rnd + '.pdfを出力しました!'
            url = str(request.META.get("HTTP_HOST"))
            params['file'] = 'http://' + url + '/diary/media/売上管理表PDF/' + str(rnd) + '.pdf'
        if 'btn-c' in request.POST:
            params['bank'] = ClientList.objects.get(k_number=params['number']).sales_management
        if 'btn-r' in request.POST:
            params['bank'] = request.POST['bank']
        rs = SalesManagement.objects.select_related().filter(
            year=params['year'], k_number__sales_management=params['bank']).order_by('k_number_id')
        kei_sum = 0
        for i, r in enumerate(rs):
            kei = 0
            """kei = r.m1 + r.m2 + r.m3 + r.m4 + r.m5 + r.m6 + r.m7 + r.m8 + r.m9 + r.m10 + r.m11+ r.m12 + \
                  r.first_tarm + r.current_term"""
            # sqlで集計したほうが良いかもしれない
            kei += r.m1 if r.m1 is not None else 0
            kei += r.m2 if r.m2 is not None else 0
            kei += r.m3 if r.m3 is not None else 0
            kei += r.m4 if r.m4 is not None else 0
            kei += r.m5 if r.m5 is not None else 0
            kei += r.m6 if r.m6 is not None else 0
            kei += r.m7 if r.m7 is not None else 0
            kei += r.m8 if r.m8 is not None else 0
            kei += r.m9 if r.m9 is not None else 0
            kei += r.m10 if r.m10 is not None else 0
            kei += r.m11 if r.m11 is not None else 0
            kei += r.m12 if r.m12 is not None else 0
            kei += r.first_term if r.first_term is not None else 0
            kei += r.current_term if r.current_term is not None else 0
            kei_sum += kei
            initial_dict = dict(year=r.year,
                                number=r.k_number_id,
                                k_name=r.k_number.k_name,
                                bank=r.k_number.sales_management,
                                m1=r.m1,
                                m2=r.m2,
                                m3=r.m3,
                                m4=r.m4,
                                m5=r.m5,
                                m6=r.m6,
                                m7=r.m7,
                                m8=r.m8,
                                m9=r.m9,
                                m10=r.m10,
                                m11=r.m11,
                                m12=r.m12,
                                first_tarm=r.first_tarm,
                                current_term=r.current_term,
                                kei=kei
                                )
            forms.append(SalesManagementForm(initial=initial_dict))
        params['sum'] = kei_sum
        params['form'] = form
        params['forms'] = forms
    else:
        params['form'] = SalesManagementForm()

    params['form'].fields['number_choice'].choices = defs.number_choice()
    return render(request, 'sales_management.html', params)
