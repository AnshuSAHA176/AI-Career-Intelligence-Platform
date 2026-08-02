from django.db import models
from config.settings import AUTH_USER_MODEL
class ChatSeasion(models.Model):
    user=models.ForeignKey(AUTH_USER_MODEL,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

class ChatMessage(models.Model):
    session=models.ForeignKey(ChatSeasion,on_delete=models.CASCADE,related_name="messages")
    role=models.CharField(max_length=20)
    content=models.TextField()
    tool_call_id=models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    tool_calls = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)