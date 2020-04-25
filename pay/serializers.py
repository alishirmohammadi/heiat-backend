from rest_framework import serializers

from .models import *


class PaymentInRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'numberOfInstallment', 'amount', 'refId', 'saleRefId', 'takingDate', 'success')


class ExpenseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ('expense_name', 'address', 'id', 'image_url', 'contribution')
