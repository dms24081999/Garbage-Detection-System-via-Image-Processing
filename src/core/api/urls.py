from django.urls import path, include
from .views import (
    CurrentUserAPIView,
    UserView,
    GarbageDataView,
    GoogleLogin,
    DeleteAllUnexpiredSessionsForUser

)
from rest_framework import routers
router = routers.DefaultRouter()
router.register('user', UserView)
router.register('garbage', GarbageDataView)

app_name = 'core-api'

urlpatterns = [
    path('user/current/details/', CurrentUserAPIView.as_view(),name='current-user-api'),
    path('', include(router.urls)),
    path('user/sessions/all/delete/', DeleteAllUnexpiredSessionsForUser.as_view(),name='del'),
    path('user/google/', GoogleLogin.as_view(), name='google_login'),

]
