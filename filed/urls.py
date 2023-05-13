
from django.urls import path
from .views import (
    fileList, FileCreateView, AssignAgentView, file_update, file_detail, file_delete,
    delete_verify, verifyDoc, track_progress
)

app_name = "files"

urlpatterns = [
    path('', fileList, name='file-list'),
    # path('landpage/', landingpage, name='land-page'),
    path('create/', FileCreateView.as_view(), name='file-create'),
    path('<int:pk>/assign-agent/', AssignAgentView.as_view(), name='assign-agent'),
    path('<int:pk>/update/', file_update, name='file-update'),
    path('<int:pk>/', file_detail   , name='file-detail'),
    path('<int:pk>/track_progress', track_progress   , name='track_progress'),
    path('<int:pk>/delete/', file_delete, name='file-delete'),
    path('<int:pk>/verifyDoc/', verifyDoc, name='verifyDoc'),
    path('<int:pk>/delete-verify', delete_verify, name='delete-verify'),
]