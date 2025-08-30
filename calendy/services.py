
import requests
from datetime import datetime, timedelta
from django.conf import settings
from .models import Appointment


def sync_calendly_appointments():
    token = settings.CALENDLY_PERSONAL_ACCESS_TOKEN
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

    user_response = requests.get("https://api.calendly.com/users/me", headers=headers)
    if user_response.status_code != 200:
        print("ERROR: Could not fetch user data from Calendly.")
        return
    organization_uri = user_response.json()['resource']['current_organization']

    one_hour_ago = (datetime.utcnow() - timedelta(hours=1)).isoformat() + "Z"
    events_url = "https://api.calendly.com/scheduled_events"
    params = {
        'organization': organization_uri,
        'min_start_time': one_hour_ago,
        'sort': 'start_time:desc',
        'count': 50
    }
    events_response = requests.get(events_url, headers=headers, params=params)
    if events_response.status_code != 200:
        print("ERROR: Could not fetch scheduled events from Calendly.")
        return
    
    events_data = events_response.json()
    new_appointments_count = 0

    
    for event in events_data['collection']:
        event_uri = event['uri']
        if not Appointment.objects.filter(event_uri=event_uri).exists():
            invitees_url = f"{event_uri}/invitees"
            invitees_response = requests.get(invitees_url, headers=headers)
            if invitees_response.status_code == 200:
                invitee = invitees_response.json()['collection'][0]
                Appointment.objects.create(
                    invitee_name=invitee['name'],
                    invitee_email=invitee['email'],
                    event_uri=event_uri,
                    start_time=event['start_time'],
                    end_time=event['end_time']
                )
                new_appointments_count += 1
    
    if new_appointments_count > 0:
        print(f"SUCCESS: Fetched and saved {new_appointments_count} new appointments.")
    else:
        print("INFO: No new appointments found in the last hour.")
    return new_appointments_count