from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter

from habits.apps import HabitsConfig
from habits.views import HabitViewSet
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView

app_name=HabitsConfig.name

router = DefaultRouter()
router.register(r'habit', HabitViewSet, basename='habit')

urlpatterns =[
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/swagger/", SpectacularSwaggerView.as_view(url_name="materials:schema")),
             ] + router.urls
