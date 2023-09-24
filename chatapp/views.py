from django.contrib.auth import logout
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from channels.layers import get_channel_layer

from .serializers import MessageSerializer, UserSerializer
from djangoChatApp.local import redis_client
from .models import Chat, User
from .serializers import ChatSerializer
from .serializers import RegistrationSerializer, LoginSerializer
from .redis_cache import get_online_users
from .utils import get_recommended_friends, RecipientNotFound, RecipientOffline


class RegistrationView(GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data
            return Response({
                "user": f"{user.id}",
                "token": f"{user.auth_token}"},
                status=status.HTTP_200_OK
            )
        return Response(
            {"error": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED
        )

class LogoutView(GenericAPIView):
    def get(self, request):
        logout(request)
        return Response(
            {"success": "Logout successfully"},
            status=status.HTTP_200_OK
        )


class OnlineUsersView(APIView):

    def get(self, request):
        online_users = get_online_users()
        return Response(online_users)


class ChatStartView(GenericAPIView):
    serializer_class = ChatSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        sender = request.user
        recipient = serializer.validated_data['recipient']
        recipient_obj = get_object_or_404(User, pk=id)
        if redis_client.sismember('online_users', recipient_obj.username):
            chat = Chat.objects.create(
                sender=sender,
                recipient=recipient
            )
            return Response({'success': 'Chat started'}, status=status.HTTP_200_OK)
        return Response({'error': 'User is offline'}, status=status.HTTP_400_BAD_REQUEST)


def validate_recipient(recipient):
    try:
        recipient = User.objects.get(username=recipient)
    except User.DoesNotExist:
        raise RecipientNotFound
    if not recipient.is_online:
        raise RecipientOffline
    return recipient


@api_view(['POST'])
def send_message(request):
    serializer = MessageSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        recipient = validate_recipient(
            serializer.validated_data['recipient']
        )
    except (RecipientNotFound, RecipientOffline) as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    message = serializer.save(sender=request.user)
    channel_layer = get_channel_layer()
    channel_layer.group_send(
        recipient.username,
        {
            'type': 'chat_message',
            'message': serializer.data
        }
    )
    return Response(serializer.data, status=status.HTTP_201_CREATED)


class SuggestedFriendsView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, user_id):
        friends = get_recommended_friends(user_id)
        serializer = UserSerializer(friends, many=True)
        return Response(serializer.data)
