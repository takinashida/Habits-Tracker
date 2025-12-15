from celery import shared_task
from habits.models import Habit
from services import send_telegram_message

@shared_task
def send_habit_reminder(habit_id):
    habit = Habit.objects.get(id=habit_id)

    message = f'⏰ Напоминание!\n\n{habit.action}'

    send_telegram_message(
        chat_id=habit.user.telegram_chat_id,
        text=message
    )
