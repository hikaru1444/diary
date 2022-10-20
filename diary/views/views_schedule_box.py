from django.shortcuts import render
from diary.forms import ScheduleBoxForm
from django.views.generic import TemplateView
import datetime
from diary.models import ScheduleBox
from diary.views import defs


def views_schedule_box(request):
    params = {'form': None, 'user': request.user}
    initial_dict = dict(name=params['user'])
    if request.method == 'POST':
        form = ScheduleBoxForm(request.POST)
        params['number'] = defs.number_post(request.POST['number'], request.POST['number_choice'])
        if 'btn-r' in request.POST:
            params['date'] = request.POST['date']
            try:
                r = ScheduleBox.objects.get(k_number_id=params['number'], date=params['date'])
                initial_dict = dict(number=r.k_number_id, date=r.date,
                                    filing_type=r.filing_type, content=r.content.replace('<br>', '\r\n'), note=r.note)
                form = ScheduleBoxForm(initial=initial_dict)
                params['check'] = '詳細を出力しました!'
            except ScheduleBox.DoesNotExist:
                params['check'] = '存在しません。'
        elif 'btn-c' in request.POST:
            params['date'] = request.POST['date']
            params['filing_type'] = request.POST['filing_type']
            params['content'] = request.POST['content']
            params['note'] = request.POST['note']
            params['content'] = params['content'].replace('\r\n', '<br>')
            try:
                u = ScheduleBox.objects.get(k_number_id=params['number'], date=params['date'])
                u.filing_type = params['filing_type']
                u.content = params['content']
                u.note = params['note']
                u.save()
                params['check'] = "変更しました!"
            except ScheduleBox.DoesNotExist:
                c = ScheduleBox(k_number_id=params['number'], date=params['date'],
                                filing_type=params['filing_type'], content=params['content'],
                                note=params['note'])
                c.save()
                params['check'] = "追加しました!"
        elif 'btn-d' in request.POST:
            params['date'] = request.POST['date']
            ScheduleBox.objects.filter(k_number_id=params['number'], date=params['date']).delete()
            params['check'] = "削除しました!"
        elif 'btn-r1' in request.POST:
            params['hyo3'] = ScheduleBox.objects.select_related().filter(
                             k_number_id=params['number']).order_by('date')
        params['form'] = form
    else:
        params['form'] = ScheduleBoxForm(initial=initial_dict)
    params['hyo'] = ScheduleBox.objects.select_related().exclude(filing_type='済み').order_by('date').reverse()
    params['hyo2'] = ScheduleBox.objects.select_related().filter(filing_type='済み').order_by('date').reverse()[:20]
    params['form'].fields['number_choice'].choices = defs.number_choice()
    return render(request, 'schedule_box.html', params)
