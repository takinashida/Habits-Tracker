from rest_framework.serializers import ValidationError

def validate_duration(value):
    if value > 120:
        raise ValidationError('Длительность привычки не может превышать 120 секунд')


def validate_period(value):
    if value < 1:
        raise ValidationError('Привычку нельзя выполнять реже, чем 1 раз в день')


def validate_habit(data):
    is_pleasant = data.get('is_pleasant')
    reward = data.get('reward')
    related_habit = data.get('related_habit')

    if is_pleasant:
        if reward or related_habit:
            raise ValidationError(
                'У приятной привычки не может быть награды или связанной привычки'
            )

    if not is_pleasant:
        if reward and related_habit:
            raise ValidationError(
                'Нельзя одновременно указывать награду и связанную привычку'
            )
