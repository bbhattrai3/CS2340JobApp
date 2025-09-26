from django.db import models
from django.conf import settings

class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    thread_id = models.CharField(max_length=100, null=True, blank=True)  # Groups messages in same thread
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username}: {self.subject}"
    
    def get_thread_messages(self):
        """Get all messages in the same thread"""
        if self.thread_id:
            return Message.objects.filter(thread_id=self.thread_id).order_by('created_at')
        return Message.objects.filter(id=self.id)
    
    def get_reply_count(self):
        """Get number of replies in this thread"""
        return self.replies.count()
