# api/tasks.py
from celery import shared_task
from .services import sync_calendly_appointments

@shared_task
def fetch_new_appointments_task():
    """
    Automatically fetch data from  calendy 
    """
    print("Starting periodic task: Fetching new appointments from Calendly...")
    sync_calendly_appointments()
    print("Periodic task finished.")