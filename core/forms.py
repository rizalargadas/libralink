from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'librarian_id',
                  'email', 'password1', 'password2')


class CustomAuthenticationForm(AuthenticationForm):
    librarian_id = forms.CharField(
        max_length=8, required=True, label='Librarian ID')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autofocus': True})
        # Define the order of fields
        self.order_fields(['username', 'librarian_id', 'password'])

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        librarian_id_form = self.cleaned_data['librarian_id']
        if not user.librarian_id == librarian_id_form:
            raise forms.ValidationError(
                "Incorrect librarian ID.", code='invalid_librarian_id')

    # def __init__(self, *args, **kwargs):
    #     super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
    #     self.order_fields(['username', 'librarian_id', 'password'])
