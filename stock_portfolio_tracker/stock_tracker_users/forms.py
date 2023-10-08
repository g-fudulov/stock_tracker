from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

UserModel = get_user_model()


class CustomRegisterUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ('email', )

    error_messages = {
        'password_mismatch': 'The passwords do not match.'
    }
