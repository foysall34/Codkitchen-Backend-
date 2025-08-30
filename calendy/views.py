from rest_framework import generics, status
from rest_framework.response import Response
from .models import ContactMessage
from .serializers import ContactMessageSerializer
from django.core.mail import send_mail
from django.conf import settings

class ContactFormCreateView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        try:
            instance = serializer.instance
            send_mail(
                subject=f"New Contact Form Submission: {instance.subject}",
                message=(
                    f"You have received a new message from your website's contact form:\n\n"
                    f"Name: {instance.name}\n"
                    f"Email: {instance.email}\n"
                    f"Phone: {instance.phone or 'Not Provided'}\n\n"
                    f"Message:\n{instance.message}"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['admin@example.com'],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Error sending email: {e}")

        saved_data = serializer.data
        custom_response = {
            "success": True,
            "message": "Thank you for reaching out! Your message has been received successfully.",
            "data": saved_data
        }
        headers = self.get_success_headers(serializer.data)
        return Response(custom_response, status=status.HTTP_201_CREATED, headers=headers)