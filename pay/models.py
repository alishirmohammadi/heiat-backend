import traceback
from datetime import datetime

from django.contrib.sites.models import Site
from django.db import models
from django.db.models import Sum
# from pysimplesoap.client import SoapClient
from zeep import Client

from program.models import Registration


class Expense(models.Model):
    is_open = models.BooleanField(default=True)
    expense_name = models.CharField(max_length=200)
    callback_url = models.URLField(max_length=300, null=True, blank=True)
    address = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        verbose_name = 'درگاه'
        verbose_name_plural = 'درگاه‌ها'

    def sum_of_money(self):
        return Payment.objects.filter(expense=self).filter(success=True).aggregate(Sum('amount'))['amount__sum']

    def __str__(self):
        return self.expense_name


# Create your models here.
class Payment(models.Model):
    registration = models.ForeignKey(Registration, null=True, related_name='payments', on_delete=models.CASCADE)
    expense = models.ForeignKey(Expense, null=True, related_name='payments', on_delete=models.CASCADE)
    numberOfInstallment = models.IntegerField(default=1, null=True)
    amount = models.IntegerField()
    refId = models.CharField(max_length=40, null=True, blank=True)
    saleRefId = models.CharField(max_length=40, null=True, blank=True)
    takingDate = models.DateTimeField(default=datetime.now)
    success = models.BooleanField(default=False)
    optional_name = models.CharField(max_length=64, null=True, blank=True)
    optional_mobile = models.CharField(max_length=12, null=True, blank=True)

    class Meta:
        verbose_name = 'پرداخت'
        verbose_name_plural = 'پرداخت ها'

    @classmethod
    def create(cls, amount, registration=None, numberOfInstallment=None, expense=None, optional_name=None,
               optional_mobile=None):
        payment = cls(amount=amount, registration=registration, numberOfInstallment=numberOfInstallment,
                      expense=expense, optional_name=optional_name, optional_mobile=optional_mobile)
        payment.save()
        for i in range(1, 6):
            try:
                client = Client("https://bpm.shaparak.ir/pgwchannel/services/pgw?wsdl")
                site = Site.objects.get_current()
                callback = 'http://' + site.domain + '/pay/payment_callback/'
                response = client.service.bpPayRequest(terminalId=870628, userName='sharifz', userPassword='az41837132',
                                                       orderId=payment.id, amount=int(amount) * 10,
                                                       localDate=datetime.now().date().strftime("%Y%m%d"),
                                                       localTime=datetime.now().time().strftime("%H%M%S"),
                                                       additionalData='zeinab', callBackUrl=callback, payerId=0)
                # response = response['bpPayRequestResult']
                print(response + ':: response')
                print('initial response:' + str(response))
                # try:
                refId = response.split(',')[1]

                payment.refId = refId
                payment.save()
                return payment
            except:
                print(traceback.format_exc())

        return payment

    def verify(self, saleRefId, original_id):
        for i in range(1, 6):
            try:
                client = Client("https://bpm.shaparak.ir/pgwchannel/services/pgw?wsdl")
                verfiy_response = client.service.bpVerifyRequest(terminalId=870628, userName='sharifz',
                                                                 userPassword='az41837132',
                                                                 orderId=original_id, saleOrderId=original_id,
                                                                 saleReferenceId=saleRefId)
                # ver_rescode = verfiy_response['bpVerifyRequestResult']
                self.verify_rescode = verfiy_response
                if verfiy_response == '0':
                    settle_response = client.service.bpSettleRequest(terminalId=870628, userName='sharifz',
                                                                     userPassword='az41837132',
                                                                     orderId=original_id, saleOrderId=original_id,
                                                                     saleReferenceId=saleRefId)
                    # settle_rescode = settle_response['bpSettleRequestResult']
                    if settle_response == '0':
                        self.success = True
                        self.saleRefId = saleRefId
                        self.save()
                        return 0
            except:
                print(traceback.format_exc())
