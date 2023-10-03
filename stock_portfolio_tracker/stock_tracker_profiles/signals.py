from django.db.models.signals import post_save
from django.dispatch import receiver
from stock_portfolio_tracker.stock_tracker_stocks.models import Profile
from stock_portfolio_tracker.stock_tracker_stocks.models import Portfolio


@receiver(post_save, sender=Profile)
def create_empty_portfolio(sender, instance, created, **kwargs):
    if created:
        Portfolio.objects.create(owner=instance, invested=0)
