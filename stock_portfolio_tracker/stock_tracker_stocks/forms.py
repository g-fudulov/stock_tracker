from django import forms
from django.core.validators import MinValueValidator




class BuyStockForm(forms.Form):
    price = forms.FloatField(required=True,
                             label='Price',
                             validators=[MinValueValidator(0.01)]
                             )
    quantity = forms.FloatField(required=True, label='Shares')


class SearchStockForm(forms.Form):
    symbol = forms.CharField(required=True, label="Ticker Symbol", max_length=8)
