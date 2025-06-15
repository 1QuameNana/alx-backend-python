from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import Message
from django.db.models import Prefetch

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