from django import forms
from django.core.validators import MinValueValidator


class BuyStockForm(forms.Form):
    price = forms.FloatField(required=True,
                             label='Buying Price',
                             validators=[MinValueValidator(0.01)],
                             widget=forms.NumberInput(attrs={'placeholder': '$'})
                             )
    quantity = forms.FloatField(required=True, label='Shares')


class SearchStockForm(forms.Form):
    symbol = forms.CharField(required=True,
                             label="Symbol",
                             max_length=8,
                             widget=forms.TextInput(attrs={'placeholder': 'Ticker Symbol'})
                             )


class SellStockForm(forms.Form):
    price = forms.FloatField(required=True,
                             label='Selling Price',
                             validators=[MinValueValidator(0.01)],
                             widget=forms.NumberInput(attrs={'placeholder': '$'})
                             )
    quantity = forms.FloatField(required=True, label='Shares')


class ResetPortfolio(forms.Form):
    reset = forms.BooleanField(required=True, initial=False, label="Confirm")
