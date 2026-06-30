from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0021_payrollsettings_saturday_short_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='late_exempted',
            field=models.BooleanField(default=False),
        ),
    ]
