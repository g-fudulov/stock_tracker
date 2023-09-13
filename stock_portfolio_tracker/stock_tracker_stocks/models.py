from django.db import models
from stock_portfolio_tracker.stock_tracker_users.models import MyUser


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=25, blank=True, null=True)
    last_name = models.CharField(max_length=25, blank=True, null=True)
    address = models.CharField(max_length=60, blank=True, null=True)


class Portfolio(models.Model):
    owner = models.OneToOneField(Profile, on_delete=models.CASCADE)
    stocks = models.ManyToManyField("Stock", through='PortfolioItem')

    def __str__(self):
        return f"Portfolio of {self.owner.user.email}"


class PortfolioItem(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    stock = models.ForeignKey("Stock", on_delete=models.CASCADE)
    quantity = models.FloatField()
    average_purchase_price = models.FloatField()

    def __str__(self):
        return f"{self.stock.symbol} - {self.quantity} shares"


class Stock(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    price = models.FloatField()

    def __str__(self):
        return self.symbol
