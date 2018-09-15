from django.conf.urls import url
from pay import views as pay_views
urlpatterns = [

    url(r'^payment_callback/$', pay_views.payment_callback),
    # url(r'^start/(?P<registration_id>\d+)/$', pay_views.start_pay),
    url(r'^terminal/$', pay_views.terminal),
    url(r'^terminal/(?P<expense_id>\d+)$', pay_views.terminal),
    url(r'^charity/$',pay_views.terminal),
    url(r'^charity/(?P<expense_id>\d+)$', pay_views.terminal),
]