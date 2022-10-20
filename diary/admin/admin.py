from django.contrib import admin
from diary.models import *
from django.contrib.admin import DateFieldListFilter
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import timedelta, date
from diary.views import defs
from django.db.models import Q


class AddMonthDateFieldListFilter(DateFieldListFilter):  # 日付フィルターに先月を追加

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        now = timezone.now()
        if timezone.is_aware(now):
            now = timezone.localtime(now)

        if isinstance(field, models.DateTimeField):
            today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        else:  # field is a models.DateField
            today = now.date()
        tomorrow = today + timedelta(days=1)
        if today.month == 12:
            next_month = today.replace(year=today.year + 1, month=1, day=1)
        else:
            next_month = today.replace(month=today.month + 1, day=1)
        next_year = today.replace(year=today.year + 1, month=1, day=1)
        self.links = (
            (_("Any date"), {}),
            (
                _("Today"),
                {
                    self.lookup_kwarg_since: str(today),
                    self.lookup_kwarg_until: str(tomorrow),
                },
            ),
            (
                _("Past 7 days"),
                {
                    self.lookup_kwarg_since: str(today - timedelta(days=7)),
                    self.lookup_kwarg_until: str(tomorrow),
                },
            ),
            (
                _("This month"),
                {
                    self.lookup_kwarg_since: str(today.replace(day=1)),
                    self.lookup_kwarg_until: str(next_month),
                },
            ),
            (
                _("先月"),
                {
                    self.lookup_kwarg_since: str(today.replace(day=1, month=today.month - 1)),
                    self.lookup_kwarg_until: str(next_month.replace(month=next_month.month - 1)),
                },
            ),
            (
                _("This year"),
                {
                    self.lookup_kwarg_since: str(today.replace(month=1, day=1)),
                    self.lookup_kwarg_until: str(next_year),
                },
            ),
        )


class workNameListFilter(admin.SimpleListFilter):
    title = _('名前')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'full_name'
    users = User.objects.all()

    def lookups(self, request, model_admin):
        look = [[None, _(request.user.last_name + request.user.first_name + "(ログイン中)")], ('all', _('全て'))]
        for user in self.users:
            look.append([user.username, str(user.last_name) + str(user.first_name)])
        return (
            look
        )

    def choices(self, changelist):
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == lookup,
                'query_string': changelist.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }

    def queryset(self, request, queryset):
        for j in self.users:
            if self.value() == j.username:
                return queryset.filter(name=j.username)
        """if self.value() in [u.username for u in self.users]:
            return queryset.filter(status=self.value())"""
        if self.value() is None:
            return queryset.filter(name=str(request.user),
                                   date__year=date.today().year)


@admin.register(Work)
class workAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        ('time', {'fields': ['in_time', 'out_time', 'rest_time', ]}),
        ('etc', {'fields': ['distance', 'note']}),
    ]
    ordering = ['name', '-date']
    list_display = ['name', 'date', 'w', 'in_time', 'out_time', 'rest_time', 'sum', 'note', 'distance']
    list_filter = [workNameListFilter, ('date', AddMonthDateFieldListFilter)]

    @staticmethod
    def get_change_form_initial_data(request):  # 追加ページの初期値を設定
        return {'name': (str(request.user))}

    @staticmethod
    def fullname(obj):
        return obj.name.first_name + obj.name.last_name


class filing_form_listInline(admin.TabularInline):
    model = FilingFormList  # filter付けたい
    fields = ['year', 'month']
    extra = 1


class filing_form_listAdmin(admin.ModelAdmin):
    list_display = ['year', 'month', 'tax_agency', 'k_number']  # 顧問先名ほしい
    list_filter = ['year', 'month', 'tax_agency']


admin.site.register(FilingFormList, filing_form_listAdmin)
"""
admins = [
    withholding_check, filing_final_tax work,
    clientList, year_adjustment, invoice, memo, filing_form_list,
    SalesManagement, officer_change, schedule_box, gift_tax, direct_payment,
]
"""
admins = [
    WithholdingCheck, FilingFinalTax,
    YearAdjustment, Invoice, Memo,
    SalesManagement, OfficerChange, ScheduleBox, GiftTax, DirectPayment
]
for i in admins:
    admin.site.register(i)


class clientListMonthListFilter(admin.SimpleListFilter):
    title = _('提出月')
    parameter_name = 'month'
    accounting_date_list = defs.accounting_date_list
    accounting_date = ['1月31日', '2月28日', '3月31日', '4月30日', '5月31日', '6月30日',
                       '7月31日', '8月31日', '9月30日', '10月31日', '11月30日', '12月31日']

    def lookups(self, request, model_admin):
        look = []
        for month in self.accounting_date:
            look.append([month, month])
        return (
            look
        )

    def queryset(self, request, queryset):
        for k_count, k in enumerate(self.accounting_date, start=1):
            if self.value() == k:
                return queryset.filter(
                    Q(report_schedule='無', consumption_tax_times='無',
                      accounting_date=self.accounting_date[k_count - 3]) |
                    Q(report_schedule='無', consumption_tax_times='1回',
                      accounting_date=self.accounting_date[k_count - 9]) |
                    Q(report_schedule='無', consumption_tax_times='3回',
                      accounting_date=self.accounting_date[k_count - 3]) |
                    Q(report_schedule='無', consumption_tax_times='3回',
                      accounting_date=self.accounting_date[k_count - 6]) |
                    Q(report_schedule='無', consumption_tax_times='3回',
                      accounting_date=self.accounting_date[k_count - 9]) |
                    Q(report_schedule='無', consumption_tax_times='3回',
                      accounting_date=self.accounting_date[k_count - 12]) |
                    Q(report_schedule='有', consumption_tax_times='無',
                      accounting_date=self.accounting_date[k_count - 9]) |
                    Q(report_schedule='無', consumption_tax_times='1回',
                      accounting_date=self.accounting_date[k_count - 3]) |
                    Q(report_schedule='有', consumption_tax_times='1回',
                      accounting_date=self.accounting_date[k_count - 9]) |
                    Q(report_schedule='有', consumption_tax_times='1回',
                      accounting_date=self.accounting_date[k_count - 3]) |
                    Q(report_schedule='有', consumption_tax_times='3回',
                      accounting_date=self.accounting_date[k_count - 3]) |
                    Q(report_schedule='有', consumption_tax_times='3回',
                      accounting_date=self.accounting_date[k_count - 6]) |
                    Q(report_schedule='有', consumption_tax_times='3回',
                      accounting_date=self.accounting_date[k_count - 9]) |
                    Q(report_schedule='有', consumption_tax_times='3回',
                      accounting_date=self.accounting_date[k_count - 12]) |
                    Q(consumption_tax_times='11回')
                )


class clientListAdmin(admin.ModelAdmin):
    inlines = [filing_form_listInline]
    list_display = ('k_number', 'k_name', 'last_update', 'create_date')
    list_filter = (clientListMonthListFilter, 'contract_cancellation', 'type', 'manager1', 'manager2', 'tax_agency')
    ordering = ['k_number']
    # form = client_detail_form
    # formfield_overrides = []


admin.site.register(ClientList, clientListAdmin)
