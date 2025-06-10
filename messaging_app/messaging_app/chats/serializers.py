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
