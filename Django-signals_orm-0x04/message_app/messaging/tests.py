from django.test import TestCase

# from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class MessageNotificationTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='alice', password='password123')
        self.user2 = User.objects.create_user(username='bob', password='password123')

    def test_message_creation_creates_notification(self):
        # Before sending the message
        self.assertEqual(Notification.objects.count(), 0)

        # Send message from user1 to user2
        message = Message.objects.create(sender=self.user1, receiver=self.user2, content='Hello, Bob!')

        # After sending, one notification should exist
        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.user, self.user2)
        self.assertEqual(notification.message, message)
        self.assertFalse(notification.is_read)

