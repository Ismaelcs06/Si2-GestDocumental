# gestdocu/validators.py
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

ext_validator = FileExtensionValidator(allowed_extensions=["pdf", "doc", "docx"])

def max_size(file_obj):
    if file_obj.size > 10 * 1024 * 1024:
        raise ValidationError("El archivo supera el tamaño máximo de 10 MB.")
