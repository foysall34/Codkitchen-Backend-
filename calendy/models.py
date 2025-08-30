from django.db import models
from django.core.mail import send_mail
from django.conf import settings

class Appointment(models.Model):
    invitee_name = models.CharField(max_length=255)
    invitee_email = models.EmailField()
    event_uri = models.CharField(max_length=255, unique=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    _original_is_approved = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_is_approved = self.is_approved

    def save(self, *args, **kwargs):
        if self.is_approved and not self._original_is_approved:
            try:
                send_mail(
                    subject='Your Appointment has been Confirmed!',
                    message=f"Hello {self.invitee_name},\n\nYour appointment scheduled for {self.start_time.strftime('%B %d, %Y at %I:%M %p UTC')} has been confirmed.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[self.invitee_email],
                    fail_silently=False,
                )
                print(f"SUCCESS: Confirmation email sent to {self.invitee_email}")
            except Exception as e:
                print(f"ERROR: Failed to send email. Error: {e}")
        super().save(*args, **kwargs)
        self._original_is_approved = self.is_approved

    def __str__(self):
        status = "Approved" if self.is_approved else "Pending"
        return f"Appointment with {self.invitee_name} - Status: {status}"
    


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True) 
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - Subject: {self.subject}"

    class Meta:
        ordering = ['-created_at']