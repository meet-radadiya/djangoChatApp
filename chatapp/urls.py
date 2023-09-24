from django.urls import path

from chatapp.consumers import ChatConsumer
from chatapp.views import RegistrationView, LoginView, OnlineUsersView, ChatStartView, send_message, \
    SuggestedFriendsView, LogoutView

urlpatterns = [
    path('api/register/', RegistrationView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/online-users/', OnlineUsersView.as_view(), name='online_users'),
    path('api/online-users/', OnlineUsersView.as_view(), name='online_users'),
    path('api/chat/start/', ChatStartView.as_view(), name='chat_start'),
    path('api/chat/send/', send_message, name='send'),
    path('api/suggested-friends/<int:user_id>/', SuggestedFriendsView.as_view(), name='suggested_friends')
]
