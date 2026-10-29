from django.apps import AppConfig


class StaffConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'staff'

    def ready(self):
        from django.db.models.signals import post_migrate
        post_migrate.connect(_register_homework_schedule, sender=self)


def _register_homework_schedule(sender, **kwargs):
    import datetime
    from django.utils import timezone
    try:
        from django_q.models import Schedule
        next_2am = timezone.make_aware(
            datetime.datetime.combine(
                datetime.date.today() + datetime.timedelta(days=1),
                datetime.time(2, 0),
            ),
            timezone.get_current_timezone(),
        )
        Schedule.objects.get_or_create(
            func='staff.tasks.sync_homework_all_schools',
            defaults={
                'schedule_type': Schedule.DAILY,
                'next_run': next_2am,
                'name': 'Homework Daily Sync (2AM)',
            },
        )
    except Exception:
        pass
