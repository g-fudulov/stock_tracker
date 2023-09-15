from django.shortcuts import get_object_or_404, render
from django.views import generic as views
from django.contrib.auth import views as auth_views
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from stock_portfolio_tracker.stock_tracker_stocks.models import Profile
from stock_portfolio_tracker.stock_tracker_users.forms import CustomRegisterUserForm

# Create your views here.
UserModel = get_user_model()


class Homepage(views.TemplateView):
    template_name = 'homepage.html'


class LoginUser(auth_views.LoginView):
    model = UserModel
    template_name = 'user/login.html'
    success_url = reverse_lazy('homepage')

    def get_success_url(self):
        return reverse_lazy("portfolio_details",
                            kwargs={
                                'portfolio_pk': self.request.user.profile.portfolio.pk
                            }
                            )


class RegisterUser(views.CreateView):
    model = UserModel
    template_name = 'user/register.html'
    form_class = CustomRegisterUserForm
    success_url = reverse_lazy('homepage')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Create a Profile instance for the newly registered user
        Profile.objects.create(user=self.object)
        login(self.request, self.object)
        return response


class LogoutUser(auth_views.LogoutView):
    # template_name = 'user/logout.html'
    pass


class DeleteUser(LoginRequiredMixin, UserPassesTestMixin, views.DeleteView):
    model = UserModel
    template_name = 'user/delete.html'
    success_url = reverse_lazy('homepage')

    def get_object(self, queryset=None):
        user_pk = self.kwargs['user_pk']
        return get_object_or_404(UserModel, pk=user_pk)

    def test_func(self):
        return self.request.user.pk == self.get_object().pk

    def handle_no_permission(self):
        return render(self.request, 'access_denied.html', status=404)


class ChangePassword(LoginRequiredMixin, UserPassesTestMixin, auth_views.PasswordChangeView):
    model = UserModel
    template_name = 'user/change_password.html'

    def get_success_url(self):
        return reverse_lazy('profile_details', kwargs={'profile_pk': self.get_object().profile.pk})

    def get_object(self, queryset=None):
        user_pk = self.kwargs['user_pk']
        return get_object_or_404(UserModel, pk=user_pk)

    def test_func(self):
        return self.request.user.pk == self.get_object().pk

    def handle_no_permission(self):
        return render(self.request, 'access_denied.html', status=404)


class ChangeEmail(LoginRequiredMixin, UserPassesTestMixin, views.UpdateView):
    model = UserModel
    template_name = 'user/change_email.html'
    fields = ['email', ]

    def get_success_url(self):
        return reverse_lazy('profile_details', kwargs={'profile_pk': self.get_object().profile.pk})

    def get_object(self, queryset=None):
        user_pk = self.kwargs['user_pk']
        return get_object_or_404(UserModel, pk=user_pk)

    def test_func(self):
        return self.request.user.pk == self.get_object().pk

    def handle_no_permission(self):
        return render(self.request, 'access_denied.html', status=404)
