from django.apps import AppConfig


class StockTrackerProfilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stock_portfolio_tracker.stock_tracker_profiles'

    def ready(self):
        import stock_portfolio_tracker.stock_tracker_profiles.signals
