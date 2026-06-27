from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0002_teachingallocation_not_first_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Teacher',
        ),
        migrations.AlterUniqueTogether(
            name='teachingallocation',
            unique_together={('teacher', 'subject', 'section', 'teacher_school')},
        ),
        migrations.AlterUniqueTogether(
            name='reservedslot',
            unique_together={('section', 'timeslot', 'school')},
        ),
    ]
