import datetime
import math
import random

from django.shortcuts import render
from japanera import EraDate
from reportlab.lib.pagesizes import A4, portrait
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from diary import forms_choices as f
from diary.forms import InvoiceCreateForm
from diary.models import Invoice
from diary.views import defs


def views_invoice_create(request):
    params = {'form': None}

    if request.method == 'POST':
        form = InvoiceCreateForm(request.POST)
        params['date'] = request.POST['date']
        params['number'] = defs.number_post(request.POST['number'], request.POST['number_choice'])
        if 'btn-c' in request.POST:
            params['content'] = request.POST['content']
            params['items'] = request.POST['items']
            params['money'] = request.POST['money'] if request.POST['money'] != '' else 0
            params['consumption'] = request.POST['consumption'] if request.POST['consumption'] != '' else 0
            params['withholding_income_tax'] = request.POST['withholding_income_tax'] if request.POST['withholding_income_tax'] != '' else 0
            params['reconstruction_tax'] = request.POST['reconstruction_tax'] if request.POST['reconstruction_tax'] != '' else 0

            Invoice(k_number_id=params['number'], date=params['date'], reward=params['content'],
                        items=params['items'], money=params['money'], consumption=params['consumption'],
                        withholding_income_tax=params['withholding_income_tax'],
                        reconstruction_tax=params['reconstruction_tax']).save()

            params['check'] = "追加しました!"
        elif 'btn-d' in request.POST:
            params['content'] = request.POST['content']
            d = Invoice.objects.filter(k_number_id=params['number'], date=params['date'])
            d.delete()
            params['check'] = "削除しました!"
        elif 'btn-p' in request.POST:  # PDF作成
            params['transfer_date'] = request.POST['transfer_date']
            ttf_file = '.\private_diary\diary\media\IPAexfont00401\ipaexg.ttf'
            pdfmetrics.registerFont(TTFont('IPAexGothic', ttf_file))
            w, h = portrait(A4)
            rnd = str(math.floor(random.random() * 100))
            cv = canvas.Canvas('./private_diary/diary/media/請求書PDF/' + rnd + '.pdf')
            font_size = 12
            cv.setFont('IPAexGothic', font_size)
            p = Invoice.objects.filter(k_number_id=params['number'], date=params['date'])
            p_mei = p[0].k_number.k_name
            juryogaku = 0
            for i in p:
                juryogaku += i.money
                juryogaku += i.reconstruction_tax
            now = datetime.date.today()
            era_date = EraDate(now.year, now.month, now.day).strftime("%-E%-O年%m月%d日")
            # era_date = era_date.strftime("%-E%-O年%m月%d日")
            # ヘッダー部分
            cv.drawRightString(w - 40, h - 30, era_date)
            # 顧問名が長いときの処理をする
            cv.drawString(20, h - 60, p_mei)
            cv.drawString(22, h - 60, "________________________________殿")
            cv.drawString(350, h - 90, f.post)
            cv.drawString(350, h - 105, f.address)
            cv.drawString(350, h - 120, f.company_name)
            cv.drawString(350, h - 135, f.tel)
            cv.drawString(350, h - 150, f.fax)
            cv.drawString(20, h - 170, "当事務所が受領する報酬は下記の通りとなります。")
            # フッター部分
            cv.drawString(30, 160, "口座振替:")
            cv.drawString(30, 125, "振込先           /     普通預金  " + f.users[1][1])
            cv.drawString(30, 110, f.number1)
            cv.drawString(30, 95, f.number2)
            cv.drawString(30, 80, f.number3)
            cv.drawString(30, 60, "よろしくお願いします。")
            # メイン部分
            # 55行出したい場合は2ぺーに20行ずつ出力し余りの5行を3ページ目に出力
            # p[][]にテーブルから取り出したデータが入っている
            # 座標やif文内の20は書類に応じて変更してください
            cv.drawString(20, h - 190, "　　　請求内容　　　　　　　　 　　内訳　　　　　　   　　金額　消費税等 源泉所得税 復興特別税")

            xlist = (20, 160, 330, 400, 450, 500, 550)
            q = 630
            ylist = (650, q)
            cv.grid(xlist, ylist)
            # lenpによりlistの長さ、差引受領額の位置を変える
            # listは後に引くylist += (q,)
            for count, i in enumerate(p):
                cv.drawString(20 + 1, h - 210 - 1 - count * 20, i.reward)
                cv.drawString(160 + 1, h - 210 - 1 - count * 20, i.items)
                cv.drawRightString(400 - 1, h - 210 - 1 - count * 20, str(i.money))
                cv.drawRightString(450 - 1, h - 210 - 1 - count * 20, str(i.consumption))
                cv.drawRightString(500 - 1, h - 210 - 1 - count * 20, str(i.withholding_income_tax))
                cv.drawRightString(550 - 1, h - 210 - 1 - count * 20, str(i.reconstruction_tax))
                q -= 20
                ylist += (q,)
            cv.grid(xlist, ylist)
            xlist = (550, 400)
            ylist = (q, q - 20)
            cv.grid(xlist, ylist)
            # 受領額を入力
            cv.drawString(400, q - 17, "差引受領額")
            cv.drawRightString(550, q - 17, str(juryogaku))
            # その他
            cv.setFont('IPAexGothic', 24)
            cv.drawCentredString(300, h - 25, "報酬計算書")

            cv.setFont('IPAexGothic', font_size)
            cv.setFillColorRGB(0, 0, 255)
            cv.setStrokeColorRGB(0, 0, 255)
            cv.drawRightString(w - 20, h - 60, f.company_name_eng)
            # 振替日がある場合はpdfの右下に青色で振替日を書き込む
            if params['transfer_date'] != '':
                cv.drawRightString(w - 60, 110, params['transfer_date'] + "ご指定の口座より")
                cv.drawRightString(w - 60, 90, "振替させていただきます。")
                xlist = (370, w - 40)
                ylist = (140, 70)
                cv.grid(xlist, ylist)
            cv.save()
            params['check'] = rnd + '.pdfを出力しました。'
            url = str(request.META.get("HTTP_HOST"))
            params['file'] = 'http://' + url + '/diary/media/請求書PDF/' + str(rnd) + '.pdf'
        params['hyo'] = Invoice.objects.filter(k_number_id=params['number'], date=params['date'])
        params['form'] = form
    else:
        params['form'] = InvoiceCreateForm()
        params['hyo'] = Invoice.objects.filter(
            date__year=datetime.date.today().year).order_by('date', 'k_number_id')
    params['form'].fields['number_choice'].choices = defs.number_choice()
    return render(request, 'invoice_create.html', params)
