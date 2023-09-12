from django import forms
from .models import Stock, PortfolioItem


# class StockForm(forms.ModelForm):
#     class Meta:
#         model = PortfolioItem
#         fields = ['stock', 'quantity']


class StockAddForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    symbol = forms.CharField(max_length=10, required=True)
    price = forms.DecimalField(max_digits=10, decimal_places=2, required=True)
    quantity = forms.IntegerField(required=True)
