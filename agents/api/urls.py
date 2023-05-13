from django.urls import path
from .views import (
    CreateAgentView, ActivateView
)


urlpatterns = [
    path('create-agent/', CreateAgentView.as_view()),
    path('activate/<uidb64>/<token>', ActivateView.as_view()),
]