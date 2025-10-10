# Authentication Forms - Core Application
# Formulários de Autenticação - Aplicação Core

"""
This module defines custom forms for authentication and user management.

Forms:
    - LoginForm: Custom login with remember_me functionality
    - RegisterForm: User registration with email validation
    - UserProfileForm: Edit user profile information
    - UserUpdateForm: Update basic user information

Features:
    - Bootstrap 5 styling on all form widgets
    - Translation support with gettext_lazy
    - Custom validation for email uniqueness
    - Placeholder text for better UX

Este módulo define formulários customizados para autenticação e gerenciamento de usuários.

Formulários:
    - LoginForm: Login customizado com funcionalidade remember_me
    - RegisterForm: Registro de usuário com validação de email
    - UserProfileForm: Editar informações do perfil de usuário
    - UserUpdateForm: Atualizar informações básicas do usuário

Recursos:
    - Estilização Bootstrap 5 em todos os widgets
    - Suporte a tradução com gettext_lazy
    - Validação customizada para unicidade de email
    - Texto placeholder para melhor UX
"""

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Category, Product, UserProfile

# Get the User model (supports custom user models)
# Obtém o modelo User (suporta modelos de usuário customizados)
User = get_user_model()


class LoginForm(AuthenticationForm):
    """
    Custom login form with Bootstrap styling and remember me functionality.
    Formulário de login customizado com estilização Bootstrap e funcionalidade remember me.

    Fields:
        username: Username or email field with autofocus
        password: Password field with Bootstrap styling
        remember_me: Optional checkbox to keep user logged in for 2 weeks

    Campos:
        username: Campo de nome de usuário ou email com autofocus
        password: Campo de senha com estilização Bootstrap
        remember_me: Checkbox opcional para manter usuário logado por 2 semanas

    Usage / Uso:
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
    """

    # Username field with Bootstrap classes and autofocus
    # Campo de username com classes Bootstrap e autofocus
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Username or Email"),
                "autofocus": True,
            }
        )
    )

    # Password field with Bootstrap classes
    # Campo de senha com classes Bootstrap
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": _("Password")}
        )
    )

    # Remember me checkbox for extended session
    # Checkbox remember me para sessão estendida
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )


class RegisterForm(UserCreationForm):
    """
    User registration form with email validation and required name fields.
    Formulário de registro de usuário com validação de email e campos de nome obrigatórios.

    Fields:
        username: Unique username (Django's built-in validation)
        email: Email address (validated for uniqueness)
        first_name: User's first name (required)
        last_name: User's last name (required)
        password1: Password (Django's built-in validators)
        password2: Password confirmation

    Campos:
        username: Nome de usuário único (validação integrada do Django)
        email: Endereço de email (validado para unicidade)
        first_name: Primeiro nome do usuário (obrigatório)
        last_name: Sobrenome do usuário (obrigatório)
        password1: Senha (validadores integrados do Django)
        password2: Confirmação de senha

    Validation:
        - Email must be unique (custom clean_email method)
        - Password must meet Django's password validators
        - All fields are required

    Validação:
        - Email deve ser único (método clean_email customizado)
        - Senha deve atender aos validadores de senha do Django
        - Todos os campos são obrigatórios

    Usage / Uso:
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # UserProfile is auto-created by signal
    """

    # Email field with uniqueness validation
    # Campo de email com validação de unicidade
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": _("Email")}
        ),
    )

    # First name field (required)
    # Campo de primeiro nome (obrigatório)
    first_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": _("First Name")}
        ),
    )

    # Last name field (required)
    # Campo de sobrenome (obrigatório)
    last_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": _("Last Name")}
        ),
    )

    class Meta:
        model = User
        # Field order for form display
        # Ordem dos campos para exibição do formulário
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )
        # Widget for username field
        # Widget para campo de username
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control", "placeholder": _("Username")}
            ),
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize form and customize password widgets.
        Inicializa formulário e customiza widgets de senha.
        """
        super().__init__(*args, **kwargs)

        # Customize password field widgets with Bootstrap classes
        # Customiza widgets de campos de senha com classes Bootstrap
        self.fields["password1"].widget = forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": _("Password")}
        )
        self.fields["password2"].widget = forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": _("Confirm Password")}
        )

    def clean_email(self):
        """
        Validate email uniqueness.
        Valida unicidade do email.

        Returns:
            str: Cleaned email address

        Retorna:
            str: Endereço de email limpo

        Raises:
            ValidationError: If email is already registered

        Lança:
            ValidationError: Se email já está registrado
        """
        email = self.cleaned_data.get("email")

        # Check if email already exists in database
        # Verifica se email já existe no banco de dados
        if User.objects.filter(email=email).exists():
            raise ValidationError(_("This email is already registered."))

        return email


class UserProfileForm(forms.ModelForm):
    """
    Form for editing user profile information.
    Formulário para editar informações do perfil do usuário.

    Fields:
        bio: Text area for user biography (max 500 chars, optional)
        avatar: Image upload field with validators for size and dimensions
        phone: Phone number with international format validation
        birth_date: Date picker for birth date (must be in past)
        city: Text input for city name
        country: Text input for country name
        website: URL input for personal website

    Campos:
        bio: Área de texto para biografia do usuário (máx 500 chars, opcional)
        avatar: Campo de upload de imagem com validadores de tamanho e dimensões
        phone: Número de telefone com validação de formato internacional
        birth_date: Seletor de data para data de nascimento (deve ser no passado)
        city: Campo de texto para nome da cidade
        country: Campo de texto para nome do país
        website: Campo de URL para website pessoal

    Features:
        - All fields are optional (nullable in model)
        - Bootstrap 5 styling on all widgets
        - HTML5 date picker for birth_date
        - File input for avatar with custom styling
        - Placeholder text for better UX

    Recursos:
        - Todos os campos são opcionais (nullable no model)
        - Estilização Bootstrap 5 em todos os widgets
        - Seletor de data HTML5 para birth_date
        - Input de arquivo para avatar com estilização customizada
        - Texto placeholder para melhor UX

    Usage / Uso:
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            # Avatar file is automatically saved to MEDIA_ROOT/avatars/
            # Arquivo avatar é automaticamente salvo em MEDIA_ROOT/avatars/
    """

    class Meta:
        model = UserProfile
        # Profile fields for editing / Campos de perfil para edição
        fields = ("bio", "avatar", "phone", "birth_date", "city", "country", "website")
        # Widget customization with Bootstrap styling / Customização de widgets com estilização Bootstrap
        widgets = {
            # Biography text area (4 rows) / Área de texto de biografia (4 linhas)
            "bio": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": _("Tell us about yourself..."),
                }
            ),
            # Avatar file input / Input de arquivo de avatar
            "avatar": forms.FileInput(attrs={"class": "form-control"}),
            # Phone number with placeholder / Número de telefone com placeholder
            "phone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": _("+1 234 567 8900")}
            ),
            # HTML5 date picker / Seletor de data HTML5
            "birth_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            # City input / Input de cidade
            "city": forms.TextInput(
                attrs={"class": "form-control", "placeholder": _("City")}
            ),
            # Country input / Input de país
            "country": forms.TextInput(
                attrs={"class": "form-control", "placeholder": _("Country")}
            ),
            # Website URL input / Input de URL de website
            "website": forms.URLInput(
                attrs={"class": "form-control", "placeholder": "https://example.com"}
            ),
        }


class UserUpdateForm(forms.ModelForm):
    """
    Form for updating basic user information.
    Formulário para atualizar informações básicas do usuário.

    Fields:
        first_name: User's first name (max 150 chars)
        last_name: User's last name (max 150 chars)
        email: Email address (validated for uniqueness)

    Campos:
        first_name: Primeiro nome do usuário (máx 150 chars)
        last_name: Sobrenome do usuário (máx 150 chars)
        email: Endereço de email (validado para unicidade)

    Validation:
        - Email must be unique among all users (excluding current user)
        - All fields follow Django's built-in User model validators

    Validação:
        - Email deve ser único entre todos os usuários (excluindo usuário atual)
        - Todos os campos seguem os validadores integrados do modelo User do Django

    Features:
        - Bootstrap 5 styling on all widgets
        - Placeholder text for better UX
        - Custom email validation to prevent duplicates
        - Preserves current user when checking email uniqueness

    Recursos:
        - Estilização Bootstrap 5 em todos os widgets
        - Texto placeholder para melhor UX
        - Validação customizada de email para prevenir duplicatas
        - Preserva usuário atual ao verificar unicidade do email

    Usage / Uso:
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            # User's basic information is updated
            # Informações básicas do usuário são atualizadas
    """

    class Meta:
        model = User
        # Basic user fields / Campos básicos do usuário
        fields = ("first_name", "last_name", "email")
        # Widget customization with Bootstrap styling / Customização de widgets com estilização Bootstrap
        widgets = {
            # First name input / Input de primeiro nome
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": _("First Name")}
            ),
            # Last name input / Input de sobrenome
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": _("Last Name")}
            ),
            # Email input / Input de email
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": _("Email")}
            ),
        }

    def clean_email(self):
        """
        Validate email uniqueness, excluding current user.
        Valida unicidade do email, excluindo usuário atual.

        Returns:
            str: Cleaned email address

        Retorna:
            str: Endereço de email limpo

        Raises:
            ValidationError: If email is already in use by another user

        Lança:
            ValidationError: Se email já está em uso por outro usuário
        """
        # Get email from form data / Obtém email dos dados do formulário
        email = self.cleaned_data.get("email")

        # Check if email exists for other users (exclude current user)
        # Verifica se email existe para outros usuários (exclui usuário atual)
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError(_("This email is already in use."))

        return email


class ProductForm(forms.ModelForm):
    """
    Form for creating and editing Product instances with validation and Bootstrap styling.
    Formulário para criar e editar instâncias de Product com validação e estilização Bootstrap.

    This form provides a complete interface for product management with:
    - Required fields: name, price
    - Optional fields: category, tags, is_active
    - Price validation (must be positive)
    - Bootstrap 5 styling for all fields
    - Bilingual labels and help texts (EN/PT-BR)

    Este formulário fornece uma interface completa para gerenciamento de produtos com:
    - Campos obrigatórios: name, price
    - Campos opcionais: category, tags, is_active
    - Validação de preço (deve ser positivo)
    - Estilização Bootstrap 5 para todos os campos
    - Labels e textos de ajuda bilíngues (EN/PT-BR)

    Usage Example / Exemplo de Uso:
        ```python
        # Create form / Criar formulário
        form = ProductForm(request.POST or None)

        # Validate and save / Validar e salvar
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            form.save_m2m()  # Save many-to-many (tags)
        ```

    Fields / Campos:
        name (str): Product name, required / Nome do produto, obrigatório
        price (Decimal): Product price, must be positive / Preço do produto, deve ser positivo
        category (FK): Optional category selection / Seleção de categoria opcional
        tags (M2M): Multiple tag selection / Seleção múltipla de tags
        is_active (bool): Product visibility toggle / Alternância de visibilidade do produto

    Validation / Validação:
        - name: Required, max 200 chars / Obrigatório, máx 200 caracteres
        - price: Required, must be positive decimal / Obrigatório, decimal positivo
        - category: Optional, filtered to active only / Opcional, filtrado apenas ativos
        - tags: Optional, multiple selection / Opcional, seleção múltipla
        - is_active: Defaults to True / Padrão True

    Notes / Notas:
        - Category queryset filtered to show only active categories
        - Categoria queryset filtrado para mostrar apenas categorias ativas
        - Tags use Ctrl/Cmd for multiple selection
        - Tags usam Ctrl/Cmd para seleção múltipla
        - All widgets use Bootstrap CSS classes
        - Todos widgets usam classes CSS do Bootstrap
    """

    class Meta:
        """Meta configuration / Configuração Meta"""

        model = Product
        fields = ["name", "price", "category", "tags", "is_active"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": _("Product name"),
                    "required": True,
                }
            ),
            "price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "0.00",
                    "step": "0.01",
                    "min": "0",
                    "required": True,
                }
            ),
            "category": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "tags": forms.SelectMultiple(
                attrs={
                    "class": "form-select",
                    "size": "5",
                }
            ),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "name": _("Name"),
            "price": _("Price"),
            "category": _("Category"),
            "tags": _("Tags"),
            "is_active": _("Active"),
        }
        help_texts = {
            "name": _("Enter the product name"),
            "price": _("Enter the product price"),
            "category": _("Select a category (optional)"),
            "tags": _("Hold Ctrl/Cmd to select multiple tags"),
            "is_active": _("Check to make product visible"),
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize form and set queryset filters.
        Inicializa formulário e define filtros de queryset.
        """
        super().__init__(*args, **kwargs)
        # Only show active categories / Mostrar apenas categorias ativas
        self.fields["category"].queryset = Category.objects.filter(is_active=True)
        self.fields["category"].required = False

    def clean_price(self):
        """
        Validate that price is positive.
        Valida que preço é positivo.
        """
        price = self.cleaned_data.get("price")
        if price and price < 0:
            raise ValidationError(_("Price must be positive."))
        return price
