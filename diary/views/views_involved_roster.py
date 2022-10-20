import datetime

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, portrait, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import random
import math
from django.shortcuts import render
from diary.forms import InvolvedRosterForm
from diary import forms_choices as f
from diary.models import ClientList
from django.db.models import Count
from japanera import Japanera, EraDate

def involved_roster(request):
    params = {'form': None}
    if request.method == 'POST':
        form = InvolvedRosterForm(request.POST)
        params['type'] = request.POST['type']
        params['tax_agency'] = request.POST['tax_agency']
        params['date'] = request.POST['date']
        ttf_file = './private_diary/diary/media/IPAexfont00401/ipaexg.ttf'
        pdfmetrics.registerFont(TTFont('IPAexGothic', ttf_file))
        w, h = portrait(A4)
        rnd = str(math.floor(random.random() * 100))
        if 'btn-p' in request.POST:
            if params['type'] == '法人以外':
                c = ClientList.objects.exclude(type='法人').filter(
                    tax_agency=params['tax_agency'], contract_cancellation='無').order_by('k_number')
            else:
                c = ClientList.objects.filter(
                    type=params['type'], tax_agency=params['tax_agency'], contract_cancellation='無'
                ).order_by('k_number')
        elif 'btn-p2' in request.POST:
            c = ClientList.objects.filter(contract_cancellation='無')
        cv = canvas.Canvas('private_diary/diary/media/関与名簿PDF/' + params['type'] + params['tax_agency'] +
                           rnd + '.pdf', pagesize=landscape(A4))
        cv.setFont('IPAexGothic', 18)
        cv.drawCentredString(400, w - 40, "税理士関与先名簿")
        cv.setFont('IPAexGothic', 12)
        xlist = (20, 290, 490, 540, 630, 740, 775, 810)
        ylist = (w - 160, w - 180, w - 200, w - 220, w - 240, w - 260, w - 280, w - 300, w - 320, w - 340, w - 360,
                 w - 380, w - 400, w - 420, w - 440, w - 460, w - 480, w - 500, w - 520, w - 540, w - 560)
        cv.grid(xlist, ylist)
        j = 0
        janera = Japanera()
        for count, p in enumerate(c, start=1):
            cv.drawString(22, w - 178 - j * 20, p.city)
            cv.drawString(292, w - 178 - j * 20, p.k_name)
            cv.drawCentredString(515, w - 178 - j * 20, p.report_category)
            cv.drawString(550, w - 178 - j * 20, p.involvement_date)
            cv.drawString(638, w - 178 - j * 20, p.form_of_involvement)
            cv.drawCentredString(757.5, w - 178 - j * 20, p.year_adjustment_check)
            cv.drawCentredString(792.5, w - 178 - j * 20, p.electronic_report)
            j += 1
            if count % 20 == 0 or count == len(c):
                cv.grid(xlist, ylist)
                cv.setFont('IPAexGothic', 18)
                cv.drawCentredString(400, w - 40, "税理士関与先名簿")
                cv.setFont('IPAexGothic', 12)
                cv.drawRightString(h - 20, w - 40, "事務所所在地　　" + f.address)
                cv.drawRightString(h - 20, w - 60, "税理士名　　" + f.users[1][1] + "　　印")
                cv.drawRightString(h - 20, w - 80, f.tel)
                b = datetime.datetime.strptime(params['date'], "%Y-%m-%d")
                cv.drawString(20, w - 40, EraDate(b.year, b.month, b.day).strftime("%-E%-O年%m月%d日"))
                cv.drawString(20, w - 60, params['type'] + " " + params['tax_agency'] + "　税務署管轄内")
                cv.drawString(20, w - 140, "住所（所在地）")
                cv.drawString(290, w - 140, "氏名(名称）")
                cv.drawString(490, w - 140, "申告区分")
                cv.drawString(540, w - 140, "関与開始")
                cv.drawString(630, w - 140, "関与形態")
                cv.drawString(740, w - 140, "消費税")
                cv.drawString(780, w - 140, "電子申告")
                cv.drawString(780, w - 158, "の利用")
                page_number = 1
                cv.drawCentredString(420, 15, str(page_number))
                cv.drawRightString(770, 15, '税理士業務処理簿(法第41条及び第48条の16)')
                if count % 20 == 0 and count != 0:
                    cv.showPage()
                    cv.setFont('IPAexGothic', 12)
                    j = 0
        cv.save()
        params['check'] = rnd + '.pdfを出力しました。'
        url = str(request.META.get("HTTP_HOST"))
        params['file'] = 'http://' + url + '/diary/media/関与名簿PDF/' + params['type'] + \
                         params['tax_agency'] + str(rnd) + '.pdf'
        params['form'] = form
    else:
        params['form'] = InvolvedRosterForm()
    params['hyo'] = ClientList.objects.select_related().filter(type='法人').values('tax_agency').annotate(
        Count('tax_agency')).order_by('tax_agency__count').reverse()
    params['hyo2'] = ClientList.objects.select_related().exclude(type='法人').values('tax_agency').annotate(
        Count('tax_agency')).order_by('tax_agency__count').reverse()

    return render(request, 'involved_roster.html', params)
