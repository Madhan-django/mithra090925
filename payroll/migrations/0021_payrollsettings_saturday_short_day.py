from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0020_payrollsettings_half_day_as_cl'),
    ]

    operations = [
        migrations.AddField(
            model_name='payrollsettings',
            name='saturday_short_day',
            field=models.BooleanField(default=False),
        ),
    ]
