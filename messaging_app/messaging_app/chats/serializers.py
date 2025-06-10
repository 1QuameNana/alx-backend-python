from rest_framework import serializers
from .models import Conversation, Message, User

class UserSerializer(serializers.ModelSerializer):
    class meta:
        model = User
        fields = ['id','username',
                  'email','avatar','bio']
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    class Meta:
        model = Message
        fields = ['id', 'sender',
                   'content', 'timestamp']
        
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'messages', 'created_at']




class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the custom User model.
    Includes basic profile fields.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'avatar']


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message model.
    Includes nested sender (User) details.
    """
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp']


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for Conversation model.
    Includes nested participants and messages.
    """
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'messages', 'created_at']


class ConversationCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a conversation.
    Accepts a list of participant user IDs.
    """
    participants = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all()
    )

    class Meta:
        model = Conversation
        fields = ['participants']


class MessageCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for sending a message to a conversation.
    Sender is automatically set to the current user.
    """
    class Meta:
        model = Message
        fields = ['conversation', 'content']
