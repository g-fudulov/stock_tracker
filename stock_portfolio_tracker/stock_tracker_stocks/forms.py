from django import forms
from django.core.validators import MinValueValidator


class StockAddForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    symbol = forms.CharField(max_length=10, required=True)
    price = forms.FloatField(required=True,
                             validators=[MinValueValidator(0.01)]
                             )
    quantity = forms.FloatField(required=True)


class BuyStockForm(forms.Form):
    price = forms.FloatField(required=True,
                             label='Price',
                             validators=[MinValueValidator(0.01)]
                             )
    quantity = forms.FloatField(required=True, label='Shares')
