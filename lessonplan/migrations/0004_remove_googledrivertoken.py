from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessonplan', '0003_googledrivertoken'),
    ]

    operations = [
        migrations.DeleteModel(
            name='GoogleDriveToken',
        ),
    ]
