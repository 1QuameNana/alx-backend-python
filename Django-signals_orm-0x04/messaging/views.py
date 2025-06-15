from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import Message
from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
@login_required
def delete_user(request):
    user = request.user
    logout(request)  # End session
    user.delete()    # Triggers cascading deletes or post_delete signal
    return redirect('account_deleted')  # Redirect to a confirmation p

def get_threaded_conversations(user):
    top_level_messages = Message.objects.filter(
        receiver=user,
        parent_message__isnull=True
    ).select_related('sender', 'receiver').prefetch_related(
        Prefetch('replies', queryset=Message.objects.select_related('sender'))
    )
    return top_level_messages


@login_required
def unread_inbox(request):
    """
    View to display unread messages for the logged-in user.
    """
    unread_messages = Message.unread.for_user(request.user)
    return render(request, 'inbox/unread_messages.html', {
        'unread_messages': unread_messages
    })


@login_required
def message_detail(request, message_id):
    """
    View to show a single message. Marks it as read if unread.
    """
    message = get_object_or_404(Message, id=message_id, receiver=request.user)

    # Mark as read if it hasn't been read yet
    if not message.read:
        message.read = True
        message.save(update_fields=['read'])

    return render(request, 'inbox/message_detail.html', {
        'message': message
    })


@login_required
def all_messages(request):
    """
    Optional: View to display all received messages.
    """
    messages = Message.objects.filter(receiver=request.user).select_related('sender').only(
        'id', 'sender', 'content', 'timestamp', 'read'
    )
    return render(request, 'inbox/all_messages.html', {
        'messages': messages
    })
