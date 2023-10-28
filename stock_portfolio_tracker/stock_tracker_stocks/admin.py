from django.contrib import admin
from models import Profile, Portfolio, PortfolioItem, Stock, Sale, Buy


# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_filter = ('user', "id", 'created')
    list_display = ('user', "id", 'created')
    search_fields = ('user', "id", 'created')
    ordering = ('-id', '-created')


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_filter = ('owner', "id",)
    list_display = ('owner', "id")
    search_fields = ('owner', "id")
    ordering = ('-id', '-invested', '-realised_pnl')


@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_filter = ('portfolio', "id")
    list_display = ('portfolio', "id")
    search_fields = ('portfolio', "id")
    ordering = ('-id',)


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_filter = ('symbol', "id")
    list_display = ('symbol', "id")
    search_fields = ('symbol', "id")
    ordering = ('-id', '-symbol')


@admin.register(Buy)
class BuyAdmin(admin.ModelAdmin):
    list_filter = ('initiator', "id")
    list_display = ('initiator', "id", 'buy_price', 'quantity_bought', 'date')
    search_fields = ('initiator', "id")
    ordering = ('-id', '-initiator', '-date')


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_filter = ('initiator', "id")
    list_display = ('initiator', "id", 'sale_price', 'quantity_sold', 'date')
    search_fields = ('initiator', "id")
    ordering = ('-id', '-initiator', '-date')
