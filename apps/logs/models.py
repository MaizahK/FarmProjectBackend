from django.db import models

class ActivityLog(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    module = models.CharField(max_length=100)  # e.g., 'Livestock', 'Inventory', 'Auth'
    username = models.CharField(max_length=150) # Captured from token
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.module}] {self.title} - {self.username}"