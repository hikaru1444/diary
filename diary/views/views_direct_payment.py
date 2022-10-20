from django.shortcuts import render
from diary.forms import DirectPaymentForm
from django.views.generic import TemplateView
import datetime
from diary.models import DirectPayment
from diary.views import defs


def views_direct_payment(self):
    params = {'form': None, 'user': self.user, 'year': datetime.date.today().year}
    if self.method == 'POST':
        form = DirectPaymentForm(self.POST)
        forms = []
        if 'btn-c' in self.POST:
            params['number'] = defs.number_post(self.POST['number'], self.POST['number_choice'])
            params['tax_type'] = self.POST['tax_type']
            try:
                DirectPayment.objects.get(year=params['year'],
                                          k_number_id=params['number'],
                                          tax_type=params['tax_type'])
                params['check'] = "既に存在します。"
            except DirectPayment.DoesNotExist:
                c = DirectPayment(year=params['year'],
                                  k_number_id=params['number'],
                                  tax_type=params['tax_type'])
                c.save()
                params['check'] = "追加しました!"
        elif 'btn-d' in self.POST:
            params['number'] = self.POST['number']
            params['tax_type'] = self.POST['tax_type']
            d = DirectPayment.objects.filter(year=params['year'],
                                             k_number_id=params['number'],
                                             tax_type=params['tax_type'])
            d.delete()
            params['check'] = "削除しました!"
        elif 'btn-u' in self.POST:
            params['number'] = self.POST['number']
            params['tax_type'] = self.POST['tax_type']
            try:
                u = DirectPayment.objects.get(year=params['year'],
                                              k_number_id=params['number'],
                                              tax_type=params['tax_type'])
                u.m1 = self.POST['m1']
                u.m2 = self.POST['m2']
                u.m3 = self.POST['m3']
                u.m4 = self.POST['m4']
                u.m5 = self.POST['m5']
                u.m6 = self.POST['m6']
                u.m7 = self.POST['m7']
                u.m8 = self.POST['m8']
                u.m9 = self.POST['m9']
                u.m10 = self.POST['m10']
                u.m11 = self.POST['m11']
                u.m12 = self.POST['m12']
                u.save()
                params['check'] = "変更しました!"
            except DirectPayment.DoesNotExist:
                params['check'] = "存在しません。"

        # どのボタンを押しても表示する
        rs = DirectPayment.objects.select_related().filter(
            year=params['year'],
        ).order_by('k_number_id', 'tax_type')
        for i, r in enumerate(rs):
            initial_dict = dict(year=r.year,
                                number=r.k_number_id,
                                k_name=r.k_number.k_name,
                                tax_type=r.tax_type,
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
                                m12=r.m12)
            forms.append(DirectPaymentForm(initial=initial_dict))
        params['form'] = form
        params['forms'] = forms
    else:
        params['form'] = DirectPaymentForm()

    params['form'].fields['number_choice'].choices = defs.number_choice()

    return render(self, 'direct_payment.html', params)
