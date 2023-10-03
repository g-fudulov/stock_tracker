# Generated by Django 4.2.5 on 2023-10-01 10:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stock_tracker_stocks', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='portfolioitem',
            name='portfolio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock_tracker_stocks.portfolio'),
        ),
        migrations.AddField(
            model_name='portfolioitem',
            name='stock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock_tracker_stocks.stock'),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='stock_tracker_stocks.profile'),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='stocks',
            field=models.ManyToManyField(through='stock_tracker_stocks.PortfolioItem', to='stock_tracker_stocks.stock'),
        ),
        migrations.AddField(
            model_name='buy',
            name='initiator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock_tracker_stocks.profile'),
        ),
        migrations.AddField(
            model_name='buy',
            name='stock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock_tracker_stocks.stock'),
        ),
    ]
