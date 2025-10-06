# Authentication Forms - Core Application
# Formulários de Autenticação - Aplicação Core

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import UserProfile

User = get_user_model()


class LoginForm(AuthenticationForm):
    """
    Custom login form with Bootstrap classes.
    Formulário de login customizado com classes Bootstrap.
    """

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Username or Email"),
                "autofocus": True,
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": _("Password")}
        )
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )


class RegisterForm(UserCreationForm):
    """
    User registration form with email and additional validation.
    Formulário de registro com email e validação adicional.
    """

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": _("Email")}
        ),
    )
    first_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": _("First Name")}
        ),
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": _("Last Name")}
        ),
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )
        widgets = {  # noqa: RUF012
            "username": forms.TextInput(
                attrs={"class": "form-control", "placeholder": _("Username")}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget = forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": _("Password")}
        )
        self.fields["password2"].widget = forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": _("Confirm Password")}
        )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError(_("This email is already registered."))
        return email


class UserProfileForm(forms.ModelForm):
    """
    Form for editing user profile information.
    Formulário para editar informações do perfil do usuário.
    """

    class Meta:
        model = UserProfile
        fields = ("bio", "avatar", "phone", "birth_date", "city", "country", "website")
        widgets = {  # noqa: RUF012
            "bio": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": _("Tell us about yourself..."),
                }
            ),
            "avatar": forms.FileInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": _("+1 234 567 8900")}
            ),
            "birth_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "city": forms.TextInput(
                attrs={"class": "form-control", "placeholder": _("City")}
            ),
            "country": forms.TextInput(
                attrs={"class": "form-control", "placeholder": _("Country")}
            ),
            "website": forms.URLInput(
                attrs={"class": "form-control", "placeholder": "https://example.com"}
            ),
        }


class UserUpdateForm(forms.ModelForm):
    """
    Form for updating basic user information.
    Formulário para atualizar informações básicas do usuário.
    """

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
        widgets = {  # noqa: RUF012
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": _("First Name")}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": _("Last Name")}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": _("Email")}
            ),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError(_("This email is already in use."))
        return email
