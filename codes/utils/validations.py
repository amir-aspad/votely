from django.core.exceptions import ValidationError
import re


def validate_username(value):
    if not re.match(r'^[a-zA-Z0-9_]+$', value):
        raise ValidationError('Username can only contain letters, numbers, and underscores.')
    if len(value) < 3:
        raise ValidationError('Username must be at least 3 characters long.')


def validate_phone(value):
    if not re.match(r'^09\d{9}$', value):
        raise ValidationError('Enter a valid phone number starting with 09 and 11 digits long.')
