from django.core.exceptions import ValidationError


def validate_positive_number(number):
    if number <= 0:
        raise ValidationError(
            'Здесь должно быть положительное число',
            params={'введённое значение': number})
