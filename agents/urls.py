from django.urls import path
from .views import (
    AgentListView, AgentCreateView, AgentDetailView, 
    AgentUpdateView, SupportCreateView, Agent_Delete, activate
)


app_name = 'agents'

urlpatterns = [
    path('', AgentListView.as_view(), name='agent-list'),
    path('<int:pk>/', AgentDetailView.as_view(), name='agent-detail'),
    path('<int:pk>/update/', AgentUpdateView.as_view(), name='agent-update'),
    path('<int:pk>/delete/', Agent_Delete, name='agent-delete'),
    path('create/', AgentCreateView.as_view(), name='agent-create'),
    path('support/', SupportCreateView.as_view(), name='support-create'),
    
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),
    
]