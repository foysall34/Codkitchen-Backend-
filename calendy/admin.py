from django.contrib import admin
from .models import Appointment
from .models import ContactMessage


admin.site.register(ContactMessage)
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('invitee_name', 'invitee_email', 'start_time', 'is_approved')
    list_filter = ('is_approved', 'start_time')
    search_fields = ('invitee_name', 'invitee_email')
    actions = ['approve_appointments']

   
    def approve_appointments(self, request, queryset):

        for appointment in queryset:
            appointment.is_approved = True
            appointment.save() 

    approve_appointments.short_description = "Approve selected appointments and send email"