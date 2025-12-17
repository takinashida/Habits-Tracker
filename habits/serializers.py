from rest_framework import serializers
from habits.models import Habit
from habits.validators import validate_habit, validate_duration, validate_period

class HabitSerializer(serializers.ModelSerializer):
    duration = serializers.IntegerField(validators=[validate_duration])
    period = serializers.IntegerField(validators=[validate_period])
    user = serializers.ReadOnlyField(source="user.id")

    class Meta:
        model = Habit
        fields = '__all__'

    def validate(self, data):
        validate_habit(data)
        return data
