from django.urls import path
from .views import views, views_work, views_sales_management, views_create_pdf, \
    views_involved_roster, views_invoice_create, views_direct_payment, views_schedule_box, LoginViews

urlpatterns = [
    path('work/', views_work, name='work'),
    path('client_search/', views.client_search, name='client_search'),
    path('involved_roster/', views_involved_roster.involved_roster, name='involved_roster'),
    path('main/', views.views_main, name='main'),
    path('client_input/', views.client_input, name='client_input'),
    path('client_detail/', views.views_client_detail, name='client_detail'),
    path('invoice_create/', views_invoice_create, name='invoice_create'),
    path('memo/', views.views_memo, name='memo'),
    path('officer_change/', views.view_officer_change, name='officer_change'),
    path('sales_management/', views_sales_management, name='sales_management'),
    path('print_request/', views.views_print_request, name='print_request'),
    path('document/', views.views_document, name='document'),
    path('direct_payment/', views_direct_payment, name='direct_payment'),
    path('schedule_box/', views_schedule_box, name='schedule_box'),
    path('login/', LoginViews.as_view(), name='login'),
    path('year_adjustment/', views_create_pdf.ViewsYearAdjustment.as_view(), name='year_adjustment'),
    path('filing/', views_create_pdf.ViewsFiling.as_view(), name='filing'),
    path('gift_tax_check/', views_create_pdf.ViewsGiftTaxCheck.as_view(), name='gift_tax_check'),
    path('withholding/', views_create_pdf.ViewsWithholding.as_view(), name='withholding'),
    path('filing_final_tax/', views_create_pdf.ViewsFilingFinalTax.as_view(), name='filing_final_tax'),
]
