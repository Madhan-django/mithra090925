from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0001_initial'),
        ('setup', '0011_homework_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='birthday_wish_config',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Happy Birthday!', max_length=200)),
                ('message', models.TextField(
                    default='Wishing {{student_name}} a very Happy Birthday! \U0001f382',
                    help_text='Use {{student_name}} to personalize the message.'
                )),
                ('time', models.TimeField()),
                ('is_active', models.BooleanField(default=True)),
                ('school', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='birthday_wish_config',
                    to='institutions.school'
                )),
            ],
        ),
    ]
