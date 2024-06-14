from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.core.validators import RegexValidator



class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Username", "class": "form-control", "id":"username_input"}),
        max_length=20,  # Ensures username length is not more than 20
        validators=[
            RegexValidator(
                r'^[a-zA-Z0-9._]+$',  # Regex allowing only letters, numbers, dot, and underscore
                'Username can only contain letters, numbers, dots, and underscores',
            ),
            RegexValidator(
                r'^[^\s]*$',  # Regex ensuring no whitespace
                'Username must not contain any whitespace',
            ),
        ],
    )
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email", "class": "form-control"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "class": "form-control"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password", "class": "form-control"}))

    class Meta:
        model = User
        fields = ['username', 'email']







class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customize form fields or labels if needed
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


