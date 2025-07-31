from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from inventory.models import StaffRecord

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email')  # override "username"

class CreateUserForm(UserCreationForm):
    staff = forms.ModelChoiceField(
        queryset=StaffRecord.objects.none(),
        required=False,
        help_text="(Optional) Select a staff to auto-fill name and email."
    )

    full_name = forms.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = ['staff', 'email', 'full_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['staff'].queryset = StaffRecord.objects.filter(user_account_created=False)

    def clean(self):
        cleaned_data = super().clean()
        staff = cleaned_data.get('staff')
        email = cleaned_data.get('email')
        full_name = cleaned_data.get('full_name')

        if not staff and (not email or not full_name):
            raise forms.ValidationError("Please either select a staff or manually enter email and full name.")

        return cleaned_data
