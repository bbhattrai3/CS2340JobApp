from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('sent/', views.sent_messages, name='sent_messages'),
    path('message/<int:message_id>/', views.message_detail, name='message_detail'),
    path('send/<str:recipient_username>/', views.send_message, name='send_message'),
    path('send/<str:recipient_username>/reply/<int:parent_id>/', views.send_message, name='reply_message'),
]
