# from django.db import models
#
# from stock_portfolio_tracker.stock_tracker_users.models import MyUser
# from stock_portfolio_tracker.stock_tracker_stocks.models import Portfolio
#
#
# # Create your models here.
#
#
# class Profile(models.Model):
#     user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=25, blank=True, null=True)
#     last_name = models.CharField(max_length=25, blank=True, null=True)
#     address = models.CharField(max_length=60, blank=True, null=True)
#     # portfolio = models.OneToOneField("Portfolio", on_delete=models.CASCADE, blank=True, null=True)
