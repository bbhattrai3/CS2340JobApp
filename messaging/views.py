from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
import uuid
from .models import Message
from .forms import MessageForm
from accounts.models import User

@login_required
def inbox(request):
    received_messages = Message.objects.filter(recipient=request.user)
    return render(request, 'messaging/inbox.html', {'messages': received_messages})

@login_required
def sent_messages(request):
    sent_messages = Message.objects.filter(sender=request.user)
    return render(request, 'messaging/sent_messages.html', {'messages': sent_messages})

@login_required
def message_detail(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    
    # Mark as read if recipient is viewing
    if message.recipient == request.user:
        message.is_read = True
        message.save()
    
    # Get all messages in the thread
    thread_messages = message.get_thread_messages()
    
    return render(request, 'messaging/message_detail.html', {
        'message': message,
        'thread_messages': thread_messages
    })

@login_required
def send_message(request, recipient_username, parent_id=None):
    recipient = get_object_or_404(User, username=recipient_username)
    parent_message = None
    
    if parent_id:
        parent_message = get_object_or_404(Message, id=parent_id)
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message_type = form.cleaned_data.get('message_type', 'internal')
            
            if message_type == 'email':
                # Send external email
                try:
                    subject = form.cleaned_data['subject']
                    content = form.cleaned_data['content']
                    
                    # Add threading info if replying
                    if parent_message:
                        if not subject.startswith('Re: '):
                            subject = f"Re: {subject}"
                        content = f"Reply to: {parent_message.subject}\n\n{content}"
                    
                    # Send email
                    send_mail(
                        subject=f"Message from {request.user.username} - {subject}",
                        message=f"From: {request.user.username} ({request.user.email})\n\n{content}",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[recipient.email],
                        fail_silently=False,
                    )
                    messages.success(request, f'Email sent successfully to {recipient.email}!')
                except Exception as e:
                    messages.error(request, f'Failed to send email: {str(e)}')
            else:
                # Send internal message
                message = form.save(commit=False)
                message.sender = request.user
                message.recipient = recipient
                
                # Handle threading
                if parent_message:
                    message.parent = parent_message
                    message.thread_id = parent_message.thread_id or str(parent_message.id)
                    # Add "Re: " prefix if not already present
                    if not message.subject.startswith('Re: '):
                        message.subject = f"Re: {message.subject}"
                else:
                    # New thread
                    message.thread_id = str(uuid.uuid4())
                
                message.save()
                messages.success(request, 'Message sent successfully!')
            
            return redirect('messaging:inbox')
    else:
        # Pre-fill form for replies
        initial_data = {}
        if parent_message:
            initial_data['subject'] = f"Re: {parent_message.subject}"
        form = MessageForm(initial=initial_data)
    
    return render(request, 'messaging/send_message.html', {
        'form': form, 
        'recipient': recipient,
        'parent_message': parent_message
    })
