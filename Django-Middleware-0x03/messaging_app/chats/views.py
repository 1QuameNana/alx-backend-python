from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import (
    ConversationSerializer,
    ConversationCreateSerializer,
    MessageSerializer,
    MessageCreateSerializer
)


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating conversations.
    Uses different serializers for list vs create.
    """
    queryset = Conversation.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return ConversationCreateSerializer
        return ConversationSerializer

    def get_queryset(self):
        """
        Return conversations that the current user participates in.
        """
        return self.queryset.filter(participants=self.request.user)

    def perform_create(self, serializer):
        """
        Adds the current user to the participants list on creation.
        """
        conversation = serializer.save()
        if self.request.user not in conversation.participants.all():
            conversation.participants.add(self.request.user)
class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and sending messages within conversations.
    """
    queryset = Message.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return MessageCreateSerializer
        return MessageSerializer

    def get_queryset(self):
        """
        Return messages in conversations the user is a participant of.
        """
        return self.queryset.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        """
        Automatically sets the current user as the sender of the message.
        """
        serializer.save(sender=self.request.user)
