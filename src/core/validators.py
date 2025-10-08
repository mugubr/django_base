# Custom Validators - Core Application
# Validadores Customizados - Aplicação Core

"""
This module defines custom validators for Django form and model fields.

Features:
    - Phone number validation (international format support)
    - CPF validation (Brazilian tax ID)
    - Image file validators (size, dimensions)
    - URL validators (YouTube, general URLs)
    - Date validators (future, past, age verification)
    - Regex validators (username, slug, hex color)

Este módulo define validadores customizados para campos Django.

Recursos:
    - Validação de número de telefone (suporte a formato internacional)
    - Validação de CPF (documento brasileiro)
    - Validadores de arquivo de imagem (tamanho, dimensões)
    - Validadores de URL (YouTube, URLs gerais)
    - Validadores de data (futuro, passado, verificação de idade)
    - Validadores regex (username, slug, cor hex)

Examples:
    Phone validation:
        class UserProfile(models.Model):
            phone = models.CharField(
                max_length=20,
                validators=[phone_validator]
            )

    Image validation:
        avatar = models.ImageField(
            upload_to='avatars/',
            validators=[validate_image_size, validate_image_dimensions]
        )

    Age verification:
        birth_date = models.DateField(
            validators=[validate_past_date, validate_min_age(18)]
        )

    CPF validation:
        cpf = models.CharField(
            max_length=14,
            validators=[cpf_validator]
        )
"""

import re

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

# Phone Number Validators / Validadores de Número de Telefone


class PhoneNumberValidator:
    """
    Validates phone numbers with international format support.
    Valida números de telefone com suporte a formato internacional.

    Accepts:
        - +55 11 98765-4321
        - (11) 98765-4321
        - 11987654321

    Usage:
        from core.validators import PhoneNumberValidator

        class MyModel(models.Model):
            phone = models.CharField(
                max_length=20,
                validators=[PhoneNumberValidator()]
            )
    """

    def __init__(self, message=None):
        self.message = message or _(
            "Enter a valid phone number. "
            "Formats: +55 11 98765-4321, (11) 98765-4321, or 11987654321"
        )

    def __call__(self, value):
        # Remove common formatting characters
        # Remove caracteres de formatação comuns
        cleaned = (
            value.replace(" ", "")
            .replace("-", "")
            .replace("(", "")
            .replace(")", "")
            .replace("+", "")
        )

        # Check if it's all digits
        # Verifica se são todos dígitos
        if not cleaned.isdigit():
            raise ValidationError(self.message, code="invalid_phone")

        # Brazilian phone numbers have 10-11 digits (with area code)
        # Números brasileiros têm 10-11 dígitos (com DDD)
        if len(cleaned) < 10 or len(cleaned) > 15:
            raise ValidationError(
                _("Phone number must have between 10 and 15 digits."),
                code="invalid_phone_length",
            )


phone_validator = PhoneNumberValidator()


# CPF Validator (Brazilian Tax ID) / Validador de CPF


class CPFValidator:
    """
    Validates Brazilian CPF (Cadastro de Pessoas Físicas).
    Valida CPF brasileiro.

    Usage:
        from core.validators import CPFValidator

        class UserProfile(models.Model):
            cpf = models.CharField(
                max_length=14,
                validators=[CPFValidator()]
            )
    """

    def __init__(self, message=None):
        self.message = message or _("Enter a valid CPF number.")

    def __call__(self, value):
        # Remove formatting
        # Remove formatação
        cpf = re.sub(r"[^0-9]", "", value)

        # Check length
        # Verifica comprimento
        if len(cpf) != 11:
            raise ValidationError(self.message, code="invalid_cpf")

        # Check if all digits are the same
        # Verifica se todos os dígitos são iguais
        if cpf == cpf[0] * 11:
            raise ValidationError(self.message, code="invalid_cpf")

        # Validate check digits
        # Valida dígitos verificadores
        def calculate_digit(cpf_partial, weight):
            total = sum(
                int(digit) * w for digit, w in zip(cpf_partial, weight, strict=False)
            )
            remainder = total % 11
            return 0 if remainder < 2 else 11 - remainder

        # First digit
        # Primeiro dígito
        weight1 = range(10, 1, -1)
        digit1 = calculate_digit(cpf[:9], weight1)
        if int(cpf[9]) != digit1:
            raise ValidationError(self.message, code="invalid_cpf")

        # Second digit
        # Segundo dígito
        weight2 = range(11, 1, -1)
        digit2 = calculate_digit(cpf[:10], weight2)
        if int(cpf[10]) != digit2:
            raise ValidationError(self.message, code="invalid_cpf")


cpf_validator = CPFValidator()


# Image File Validators / Validadores de Arquivo de Imagem


def validate_image_size(image):
    """
    Validates that an image file is not too large.
    Valida que um arquivo de imagem não é muito grande.

    Args:
        image: ImageField file

    Raises:
        ValidationError: If image is larger than 5MB

    Usage:
        class UserProfile(models.Model):
            avatar = models.ImageField(
                upload_to='avatars/',
                validators=[validate_image_size]
            )
    """
    max_size_mb = 5
    max_size_bytes = max_size_mb * 1024 * 1024  # 5MB in bytes

    if image.size > max_size_bytes:
        raise ValidationError(
            _(f"Image file too large. Maximum size is {max_size_mb}MB."),
            code="image_too_large",
        )


def validate_image_dimensions(image):
    """
    Validates image dimensions are within acceptable range.
    Valida que as dimensões da imagem estão dentro do intervalo aceitável.

    Args:
        image: ImageField file

    Raises:
        ValidationError: If image dimensions are invalid

    Usage:
        avatar = models.ImageField(
            upload_to='avatars/',
            validators=[validate_image_dimensions]
        )
    """
    from PIL import Image as PILImage

    # Open image
    # Abre imagem
    img = PILImage.open(image)
    width, height = img.size

    # Min dimensions
    # Dimensões mínimas
    min_width = 100
    min_height = 100

    # Max dimensions
    # Dimensões máximas
    max_width = 4000
    max_height = 4000

    if width < min_width or height < min_height:
        raise ValidationError(
            _(
                f"Image dimensions too small. Minimum: {min_width}x{min_height}px. "
                f"Current: {width}x{height}px."
            ),
            code="image_too_small",
        )

    if width > max_width or height > max_height:
        raise ValidationError(
            _(
                f"Image dimensions too large. Maximum: {max_width}x{max_height}px. "
                f"Current: {width}x{height}px."
            ),
            code="image_too_large",
        )


# URL Validators / Validadores de URL


def validate_youtube_url(value):
    """
    Validates that a URL is a valid YouTube video URL.
    Valida que uma URL é uma URL de vídeo do YouTube válida.

    Args:
        value: URL string

    Raises:
        ValidationError: If URL is not a valid YouTube URL

    Usage:
        video_url = models.URLField(validators=[validate_youtube_url])
    """
    youtube_pattern = r"^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$"

    if not re.match(youtube_pattern, value):
        raise ValidationError(
            _("Enter a valid YouTube URL."),
            code="invalid_youtube_url",
        )


# Custom Business Logic Validators / Validadores de Lógica de Negócio Customizada


def validate_future_date(value):
    """
    Validates that a date is in the future.
    Valida que uma data está no futuro.

    Args:
        value: Date or datetime object

    Raises:
        ValidationError: If date is not in the future

    Usage:
        event_date = models.DateField(validators=[validate_future_date])
    """
    from django.utils import timezone

    if value <= timezone.now().date():
        raise ValidationError(
            _("Date must be in the future."),
            code="past_date",
        )


def validate_past_date(value):
    """
    Validates that a date is in the past.
    Valida que uma data está no passado.

    Args:
        value: Date or datetime object

    Raises:
        ValidationError: If date is not in the past

    Usage:
        birth_date = models.DateField(validators=[validate_past_date])
    """
    from django.utils import timezone

    if value >= timezone.now().date():
        raise ValidationError(
            _("Date must be in the past."),
            code="future_date",
        )


def validate_min_age(min_age=18):
    """
    Returns a validator that checks if age is at least min_age.
    Retorna um validador que verifica se a idade é pelo menos min_age.

    Args:
        min_age: Minimum age required (default: 18)

    Returns:
        Validator function

    Usage:
        birth_date = models.DateField(validators=[validate_min_age(21)])
    """

    def validator(value):
        from datetime import date

        today = date.today()
        age = (
            today.year
            - value.year
            - ((today.month, today.day) < (value.month, value.day))
        )

        if age < min_age:
            raise ValidationError(
                _(f"You must be at least {min_age} years old."),
                code="age_too_young",
            )

    return validator


# Regex Validators / Validadores Regex


# Username validator (alphanumeric, underscore, hyphen)
# Validador de nome de usuário (alfanumérico, underscore, hífen)
username_validator = RegexValidator(
    regex=r"^[a-zA-Z0-9_-]+$",
    message=_("Username can only contain letters, numbers, underscores, and hyphens."),
    code="invalid_username",
)

# Slug validator (lowercase alphanumeric, hyphen)
# Validador de slug (alfanumérico minúsculo, hífen)
slug_validator = RegexValidator(
    regex=r"^[a-z0-9-]+$",
    message=_("Slug can only contain lowercase letters, numbers, and hyphens."),
    code="invalid_slug",
)

# Hex color validator (#RRGGBB)
# Validador de cor hex (#RRGGBB)
hex_color_validator = RegexValidator(
    regex=r"^#[0-9A-Fa-f]{6}$",
    message=_("Enter a valid hex color code (e.g., #FF5733)."),
    code="invalid_hex_color",
)
