from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [

    url(r'^payment_callback/$', 'pay.views.payment_callback'),
    url(r'^start/(?P<registration_id>\d+)/$', 'pay.views.start_pay'),
    url(r'^charity/$', 'pay.views.charity'),
    url(r'^charity/(?P<expense_id>\d+)$', 'pay.views.charity'),
]