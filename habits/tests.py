from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from habits.models import Habit



# Create your tests here.
class HabitTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="test",
            email="test@example.com",
            password="1234"
        )
        self.client.force_authenticate(user=self.user)

        self.habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="08:00",
            action="Отжимания",
            duration=60,
            period=1
        )


    def test_get_habit_list(self):
        url = reverse("habits:habit-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data["results"]) >= 1)

    def test_create_habit(self):
        url = reverse("habits:habit-list")

        data = {
            "user": self.user,
            "place": "Дом",
            "time": "14:19:00",
            "action": "Читать по 20 минут",
            "is_pleasant": False,
            "period": 7,
            "reward": "Напиток",
            "duration": 90,
            "is_public": True
}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 2)

    def test_habit_duration_validation(self):
        url = reverse("habits:habit-list")

        data = {
            "place": "Дом",
            "time": "10:00",
            "action": "Планка",
            "duration": 500,
            "period": 1
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_public_habit_visible(self):
        public_habit = Habit.objects.create(
            user=self.user,
            place="Парк",
            time="07:00",
            action="Ходьба",
            duration=60,
            period=1,
            is_public=True
        )

        url = reverse("habits:habit-list")
        response = self.client.get(url)

        actions = [item["action"] for item in response.data["results"]]
        self.assertIn("Ходьба", actions)


    def test_cannot_update_foreign_habit(self):
        other_user = User.objects.create_user(
            username="enemy",
            email="enemy@example.com",
            password="1234"
        )

        foreign_habit = Habit.objects.create(
            user=other_user,
            place="Зал",
            time="12:00",
            action="Пресс",
            duration=60,
            period=1
        )

        url = reverse("habits:habit-detail", args=[foreign_habit.id])
        response = self.client.patch(url, {"action": "Хак"})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

