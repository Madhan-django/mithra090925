from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0019_payrollsettings_grace_mins'),
    ]

    operations = [
        migrations.AddField(
            model_name='payrollsettings',
            name='half_day_as_cl',
            field=models.BooleanField(default=False),
        ),
    ]
