import requests
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from stock_portfolio_tracker.stock_tracker_stocks.models import Portfolio, PortfolioItem, Stock, Profile, Sale, Buy
from django.views import generic as views
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from stock_portfolio_tracker.stock_tracker_stocks.forms import BuyStockForm, SearchStockForm, SellStockForm
from stock_portfolio_tracker.stock_tracker_stocks import helper_funcs

UserModel = get_user_model()


# Create your views here.

class PortfolioDetails(LoginRequiredMixin, UserPassesTestMixin, views.DetailView):
    model = Portfolio
    template_name = "portfolio/details.html"

    def get_object(self, queryset=None):
        pk = self.kwargs['portfolio_pk']
        return get_object_or_404(Portfolio, pk=pk)

    def test_func(self):
        return self.get_object().owner.user_id == self.request.user.pk

    def handle_no_permission(self):
        return render(
            self.request,
            'access_denied.html',
            {"error": 'You are not the owner of this portfolio!'},
            status=404
        )


@login_required(login_url=reverse_lazy('login_user'))
def add_stock_to_portfolio(request, portfolio_pk):
    portfolio = get_object_or_404(Portfolio, pk=portfolio_pk)

    if request.user.pk != portfolio.owner.user.pk:  # Check for access
        return render(
            request,
            'access_denied.html',
            {"error": 'You are not the owner of this portfolio!'}
        )

    form = SearchStockForm()
    if request.method == "POST":
        form = SearchStockForm(request.POST)
        if form.is_valid():
            symbol = form.cleaned_data['symbol']
            stock_data = helper_funcs.check_stock_exists(symbol)

            if not stock_data:
                return render(request, 'portfolio/not_existing.html')

            parsed_symbol = stock_data['data'][0]['symbol']
            parsed_name = stock_data['data'][0]['name']
            stock, created = Stock.objects.get_or_create(
                symbol=parsed_symbol,
                defaults={
                    'name': parsed_name,
                    'price': 0,
                })

            existing_portfolio_item = PortfolioItem.objects.filter(portfolio=portfolio, stock=stock).first()

            if not existing_portfolio_item:
                PortfolioItem.objects.create(
                    portfolio=portfolio,
                    stock=stock,
                    quantity=0,
                    average_purchase_price=0,
                )

            return redirect('buy_stock', portfolio_pk=portfolio_pk, stock_symbol=parsed_symbol)

    return render(request, 'portfolio/search_stock.html', {"form": form})


@login_required(login_url=reverse_lazy('login_user'))
def buy_stock(request, portfolio_pk, stock_symbol):
    portfolio = get_object_or_404(Portfolio, pk=portfolio_pk)
    stock = get_object_or_404(Stock, symbol=stock_symbol)
    portfolio_item = PortfolioItem.objects.filter(portfolio=portfolio, stock=stock).first()

    if request.user.pk != portfolio.owner.user.pk:  # Check for access
        return render(
            request,
            'access_denied.html',
            {"error": 'You are not the owner of this portfolio!'}
        )

    form = BuyStockForm()
    if request.method == "POST":
        form = BuyStockForm(request.POST)
        if form.is_valid():
            """Calculates the average price per share"""
            (new_average_purchase_price, new_quantity) = (
                helper_funcs.calculate_avg_price_per_share_buy(
                    existing_quantity=portfolio_item.quantity,
                    bought_quantity=form.cleaned_data['quantity'],
                    existing_avg_price=portfolio_item.average_purchase_price,
                    bought_price=form.cleaned_data['price']
                ))
            portfolio_item.average_purchase_price = new_average_purchase_price
            portfolio_item.quantity = new_quantity
            portfolio_item.save()

            # Creates a new buy record
            profile = get_object_or_404(Profile, portfolio=portfolio)
            Buy.objects.create(
                initiator=profile,
                stock=stock,
                quantity_bought=form.cleaned_data['quantity'],
                buy_price=form.cleaned_data['price'],
            )

            # Updates the total invested amount
            portfolio.invested += helper_funcs.format_float(form.cleaned_data['quantity'] * form.cleaned_data['price'])
            portfolio.save()

            return redirect('portfolio_details', portfolio_pk=portfolio_pk)

    return render(request, "portfolio/buy.html", {"form": form, 'portfolio_item': portfolio_item})


class RemoveStock(LoginRequiredMixin, UserPassesTestMixin, views.DeleteView):
    template_name = "portfolio/remove.html"

    def get_success_url(self):
        return reverse_lazy("portfolio_details", kwargs={"portfolio_pk": self.kwargs['portfolio_pk']})

    def get_object(self, queryset=None):
        portfolio_pk = self.kwargs['portfolio_pk']
        stock_symbol = self.kwargs['stock_symbol']
        stock = get_object_or_404(Stock, symbol=stock_symbol)
        return get_object_or_404(PortfolioItem, portfolio__id=portfolio_pk, stock=stock)

    def get_profile_of_portfolio(self):
        portfolio_pk = self.kwargs['portfolio_pk']
        portfolio = get_object_or_404(Portfolio, pk=portfolio_pk)
        return get_object_or_404(Profile, portfolio=portfolio)

    def test_func(self):
        return self.request.user.pk == self.get_profile_of_portfolio().user_id

    def handle_no_permission(self):
        return render(
            self.request,
            'access_denied.html',
            {"error": 'You are not the owner of this portfolio!'},
            status=404
        )


@login_required(login_url=reverse_lazy("login_user"))
def sell_stock(request, portfolio_pk, stock_symbol):
    portfolio = get_object_or_404(Portfolio, pk=portfolio_pk)
    stock = get_object_or_404(Stock, symbol=stock_symbol)
    portfolio_item = PortfolioItem.objects.filter(portfolio=portfolio, stock=stock).first()

    if request.user.pk != portfolio.owner.user.pk:  # Check for access
        return render(
            request,
            'access_denied.html',
            {"error": 'You are not the owner of this portfolio!'}
        )

    if not portfolio_item:
        return render(
            request,
            'access_denied.html',
            {"error": f'{stock_symbol} does not exist in your portfolio!'}
        )

    form = SellStockForm()
    if request.method == "POST":
        form = SellStockForm(request.POST)
        if form.is_valid():
            sell_price = form.cleaned_data['price']
            sell_quantity = form.cleaned_data['quantity']

            if sell_quantity > portfolio_item.quantity:
                return render(request, 'sell_error.html')

            """Calculates the realised P&L"""
            realised_pnl = helper_funcs.calculate_realised_pnl(
                existing_pnl=portfolio.realised_pnl,
                existing_avg_price=portfolio_item.average_purchase_price,
                selling_price=sell_price,
                selling_quantity=sell_quantity
            )
            portfolio.realised_pnl = realised_pnl
            portfolio.save()

            # Updates the total invested
            average_price = portfolio_item.average_purchase_price
            portfolio.invested -= helper_funcs.format_float(average_price * sell_quantity)
            if portfolio.invested <= 0.02:
                portfolio.invested = 0
            portfolio.save()

            if sell_quantity == portfolio_item.quantity:
                # Sold all shares, remove the portfolio item
                portfolio_item.delete()
            else:
                """Updates the quantity"""
                new_quantity = helper_funcs.update_quantity(
                    existing_quantity=portfolio_item.quantity,
                    selling_quantity=sell_quantity,
                )
                portfolio_item.quantity = new_quantity
                portfolio_item.save()

            # Creates a new sale record
            profile = get_object_or_404(Profile, portfolio=portfolio)
            Sale.objects.create(
                initiator=profile,
                stock=stock,
                quantity_sold=sell_quantity,
                sale_price=sell_price,
            )

            return redirect('portfolio_details', portfolio_pk=portfolio_pk)

    return render(request, 'portfolio/sell.html', {'form': form, 'portfolio_item': portfolio_item})


class SalesDetails(LoginRequiredMixin, UserPassesTestMixin, views.ListView):
    model = Sale
    template_name = 'portfolio/sales_history.html'
    paginate_by = 10

    def get_queryset(self):
        return Sale.objects.filter(initiator__id=self.kwargs['profile_pk']).order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['realised_pnl'] = get_object_or_404(Portfolio, pk=self.kwargs['portfolio_pk']).realised_pnl
        context['portfolio_pk'] = self.kwargs['portfolio_pk']
        context['profile_pk'] = self.kwargs['profile_pk']
        return context

    def test_func(self):
        return self.request.user.pk == get_object_or_404(Profile, pk=self.kwargs['profile_pk']).user_id

    def handle_no_permission(self):
        return render(
            self.request,
            'access_denied.html',
            {"error": 'You are not the owner of this portfolio details!'},
            status=404
        )


class BuysDetails(LoginRequiredMixin, UserPassesTestMixin, views.ListView):
    model = Buy
    template_name = 'portfolio/buys_history.html'
    paginate_by = 10

    def get_queryset(self):
        return Buy.objects.filter(initiator__id=self.kwargs['profile_pk']).order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['realised_pnl'] = get_object_or_404(Portfolio, pk=self.kwargs['portfolio_pk']).realised_pnl
        context['portfolio_pk'] = self.kwargs['portfolio_pk']
        context['profile_pk'] = self.kwargs['profile_pk']
        return context

    def test_func(self):
        return self.request.user.pk == get_object_or_404(Profile, pk=self.kwargs['profile_pk']).user_id

    def handle_no_permission(self):
        return render(
            self.request,
            'access_denied.html',
            {"error": 'You are not the owner of this portfolio details!'},
            status=404
        )
