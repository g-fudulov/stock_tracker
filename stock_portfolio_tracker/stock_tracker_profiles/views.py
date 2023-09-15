from django.shortcuts import get_object_or_404, render
from django.views import generic as views
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from stock_portfolio_tracker.stock_tracker_stocks.models import Profile

UserModel = get_user_model()


# Create your views here.
class ProfileDetails(LoginRequiredMixin, UserPassesTestMixin, views.DetailView):
    model = Profile
    template_name = 'profile/details.html'

    def get_object(self, queryset=None):
        profile_pk = self.kwargs['profile_pk']
        return get_object_or_404(Profile, pk=profile_pk)

    def test_func(self):
        return self.request.user.pk == self.get_object().user_id

    def handle_no_permission(self):
        return render(self.request, 'access_denied.html', status=404)


class UpdateDetails(LoginRequiredMixin, UserPassesTestMixin, views.UpdateView):
    model = Profile
    template_name = 'profile/update.html'
    fields = ['first_name', 'last_name', 'address']

    def get_success_url(self):
        return reverse_lazy('profile_details', kwargs={'profile_pk': self.get_object().pk})

    def get_object(self, queryset=None):
        profile_pk = self.kwargs['profile_pk']
        return get_object_or_404(Profile, pk=profile_pk)

    def test_func(self):
        return self.request.user.pk == self.get_object().user_id

    def handle_no_permission(self):
        return render(self.request, 'access_denied.html', status=404)
