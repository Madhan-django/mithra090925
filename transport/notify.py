from django.utils import timezone
from mobi.models import DeviceFCMToken
try:
    from firebase_admin import messaging
    _FCM_AVAILABLE = True
except ImportError:
    _FCM_AVAILABLE = False


def send_boarding_fcm(student, status, trip, route_name, stop_name, school_obj):
    """
    Push a boarding alert to a student's registered FCM devices.
    Called from boarding_mark after each record is saved.
    Only fires for Boarded / Missed status — Absent is silent.
    """
    if not _FCM_AVAILABLE:
        return

    if status == 'Boarded':
        now_str = timezone.localtime().strftime('%I:%M %p')
        trip_label = 'boarded' if trip == 'AM' else 'returned'
        title = 'Bus Update'
        body = (
            f"{student.first_name} {student.last_name} has {trip_label} "
            f"{route_name} at {stop_name} ({now_str})."
        )
    elif status == 'Missed':
        trip_label = 'missed the morning bus' if trip == 'AM' else 'missed the return bus'
        title = 'Bus Alert'
        body = (
            f"{student.first_name} {student.last_name} has {trip_label} "
            f"at {stop_name} ({route_name}). Please check."
        )
    else:
        return

    tokens = DeviceFCMToken.objects.filter(username=student.usernm)
    for device in tokens:
        try:
            msg = messaging.Message(
                notification=messaging.Notification(title=title, body=body),
                android=messaging.AndroidConfig(
                    notification=messaging.AndroidNotification(
                        icon=str(school_obj.logo) if school_obj.logo else None,
                    )
                ),
                token=device.firecmToken,
            )
            messaging.send(msg)
        except Exception as e:
            print(f"Boarding FCM error ({student.usernm}): {e}")
