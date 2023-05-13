from django.urls import path
from .views import (
    FileDetailView, FileListView, verifyDocCreateView, 
    verifyDocUpdateView, verifyDocDeleteView, AssignAgentView,
    AssignAgentRetrieveView, FileTypeView, AllFileView,

    UnderReview, ReviewView, ObservationView, NotifiedView,
    DocumentView, ActProcedureView, PersonalNotifiedView,
    PaymentView, PaymentDocView, ResolutionView, ResolutionNotificationView,
    TrackDetailView, FileDetailViewII, FileNumView, FileSearchView,
    FileNumSearchView, ResolutionNumView, CompletedStatus, LoggerView
)

urlpatterns = [
    path('files', FileListView.as_view(), name='file-list'),
    path('all-files', AllFileView.as_view()),
    path('logger-all', LoggerView.as_view()),

    # path('file-search/', FileSearchView.as_view(), name='file-list'),
    path('file-search/<pk>', FileNumSearchView.as_view()),
    path('files/<pk>/', FileDetailView.as_view(), name='file-detail'),
    path('filesii/<pk>/', FileDetailViewII.as_view()),
    path('completed/<pk>/', CompletedStatus.as_view()),

    path('verify/create/', verifyDocCreateView.as_view(), name='verify-create'),
    path('verify/<pk>/', verifyDocUpdateView.as_view(), name='verify'),
    path('verify/delete/<pk>/', verifyDocDeleteView.as_view(), name='address-delete'),

    path('assign-agent/<int:pk>/', AssignAgentView.as_view(), name='assign-agent'),
    path('assign-retrieve/', AssignAgentRetrieveView.as_view(), name='assign-retrieve'),
    path('file-type/', FileTypeView.as_view(), name='file-type'),
    path('file-num/', FileNumView.as_view()),
    path('resolution-num/', ResolutionNumView.as_view()),


    # =============== track progresss ====================
    path('under-review/<int:pk>/', UnderReview.as_view() ),
    path('review/<int:pk>/', ReviewView.as_view() ),
    path('observation/<int:pk>/', ObservationView.as_view() ),
    path('notified/<int:pk>/', NotifiedView.as_view() ),
    path('document/<int:pk>/', DocumentView.as_view() ),
    path('act-procedure/<int:pk>/', ActProcedureView.as_view() ),
    path('personal-notified/<int:pk>/', PersonalNotifiedView.as_view() ),
    path('payment/<int:pk>/', PaymentView.as_view() ),
    path('payment-doc/<int:pk>/', PaymentDocView.as_view() ),
    path('resolution/<int:pk>/', ResolutionView.as_view() ),
    path('resolution-notification/<int:pk>/', ResolutionNotificationView.as_view() ),
    path('track-detail/<int:pk>/', TrackDetailView.as_view() ),
]