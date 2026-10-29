from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('institutions', '0009_schoolmenupermission'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupMenuPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admission', models.BooleanField(default=True)),
                ('students', models.BooleanField(default=True)),
                ('staffs', models.BooleanField(default=True)),
                ('academics', models.BooleanField(default=True)),
                ('timetable', models.BooleanField(default=True)),
                ('finance', models.BooleanField(default=False)),
                ('payroll', models.BooleanField(default=False)),
                ('transport', models.BooleanField(default=False)),
                ('hostel', models.BooleanField(default=False)),
                ('petty_cash', models.BooleanField(default=False)),
                ('examination', models.BooleanField(default=True)),
                ('question_bank', models.BooleanField(default=False)),
                ('library', models.BooleanField(default=True)),
                ('assets', models.BooleanField(default=False)),
                ('inventory', models.BooleanField(default=False)),
                ('visitors', models.BooleanField(default=False)),
                ('reports', models.BooleanField(default=False)),
                ('jacob_reports', models.BooleanField(default=False)),
                ('configurations', models.BooleanField(default=False, help_text='Settings/Configurations sidebar section')),
                ('students_authenticate', models.BooleanField(default=False, help_text='Student login credential management')),
                ('students_promote', models.BooleanField(default=False, help_text='Student class promotion')),
                ('students_transfer', models.BooleanField(default=False, help_text='Student transfer')),
                ('group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='menu_permission', to='auth.group')),
            ],
            options={
                'verbose_name': 'Group Menu Permission',
                'verbose_name_plural': 'Group Menu Permissions',
            },
        ),
    ]
