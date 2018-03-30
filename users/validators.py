from django.core.validators import RegexValidator


class UsernameValidator(RegexValidator):
    regex = r'^\w+$'
    message = "Alphanumeric characters only."
