from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from habits.models import Habit
from habits.pagination import HabitPagination
from habits.serializers import HabitSerializer
from habits.permissions import IsOwner
from habits.tasks import send_habit_reminder
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json

# Create your views here.
class HabitViewSet(ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HabitPagination

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        habit = serializer.save(user=self.request.user)
        crontab, _ = CrontabSchedule.objects.get_or_create(
            minute=str(habit.time.minute),
            hour=str(habit.time.hour),
            day_of_month=f'*/{habit.period}',
            month_of_year='*',
            day_of_week='*',
        )


        PeriodicTask.objects.create(
            crontab=crontab,
            name=f'habit-{habit.id}',
            task='habits.tasks.send_habit_reminder',
            args= json.dumps([habit.id]),
        )

    def perform_destroy(self, instance):
        PeriodicTask.objects.filter(name=f'habit-{instance.id}').delete()
        instance.delete()

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOwner()]
        return super().get_permissions()

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def public(self, request):
        queryset = Habit.objects.filter(is_public=True)
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)




