from django.core.exceptions import ValidationError
import re

class CustomPasswordValidator:
    def __init__(self, min_length=8, special_characters=None):
        self.min_length = min_length
        self.special_characters = special_characters or ['@', '&', '$', '%', '!', '#', '*']

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                f"Пароль должен содержать не менее {self.min_length} символов."
            )
        if not any(char.isdigit() for char in password):
            raise ValidationError(
                f"Пароль должен содержать хотя бы одну цифру."
            )    
        if not any(char in password for char in self.special_characters):
            raise ValidationError(
                "Пароль должен содержать хотя бы один из следующих символов: " + ", ".join(self.special_characters)
            )

    def get_help_text(self):
        return f"Ваш пароль должен содержать не менее {self.min_length} символов и включать хотя бы один из следующих символов: {', '.join(self.special_characters)}"
