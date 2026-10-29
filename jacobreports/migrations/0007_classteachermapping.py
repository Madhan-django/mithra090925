from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0001_initial'),
        ('jacobreports', '0006_replace_late_evening_class_fields'),
        ('staff', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassTeacherMapping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institutions.school')),
                ('incharge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supervised_teachers', to='staff.staff')),
                ('class_teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incharge_mappings', to='staff.staff')),
            ],
            options={
                'unique_together': {('incharge', 'class_teacher')},
            },
        ),
    ]
