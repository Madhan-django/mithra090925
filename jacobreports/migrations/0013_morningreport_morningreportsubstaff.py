import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jacobreports', '0012_inchargereport_breakfast_count_and_more'),
        ('institutions', '0001_initial'),
        ('staff', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MorningReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('overall_status', models.CharField(choices=[('Closed', 'Closed'), ('Open', 'Open'), ('In-Progress', 'In-Progress'), ('Issue', 'Issue')], default='Closed', max_length=20)),
                ('report_date', models.DateField()),
                ('senior_vp_time', models.CharField(blank=True, max_length=10, null=True)),
                ('hr_sec_vp_time', models.CharField(blank=True, max_length=10, null=True)),
                ('high_school_vp_time', models.CharField(blank=True, max_length=10, null=True)),
                ('primary_vp_time', models.CharField(blank=True, max_length=10, null=True)),
                ('office_incharge1_time', models.CharField(blank=True, max_length=10, null=True)),
                ('office_incharge2_time', models.CharField(blank=True, max_length=10, null=True)),
                ('maintenance_incharge_time', models.CharField(blank=True, max_length=10, null=True)),
                ('morning_duty_attended', models.CharField(blank=True, max_length=20, null=True)),
                ('morning_duty_not_attended', models.CharField(blank=True, max_length=20, null=True)),
                ('office_opened_time', models.CharField(blank=True, max_length=10, null=True)),
                ('parent_complaints', models.TextField(blank=True, null=True)),
                ('teachers_present', models.PositiveIntegerField(default=0)),
                ('teachers_absent', models.PositiveIntegerField(default=0)),
                ('absentees_teachers', models.TextField(blank=True, null=True)),
                ('absentees_non_teaching', models.TextField(blank=True, null=True)),
                ('late_comers_teachers', models.TextField(blank=True, null=True)),
                ('late_comers_spl_duty', models.TextField(blank=True, null=True)),
                ('late_pupils_primary', models.CharField(blank=True, max_length=20, null=True)),
                ('late_pupils_high_school', models.CharField(blank=True, max_length=20, null=True)),
                ('late_pupils_hr_sec', models.CharField(blank=True, max_length=20, null=True)),
                ('late_pupils_total', models.CharField(blank=True, max_length=20, null=True)),
                ('general_instruction_by', models.TextField(blank=True, null=True)),
                ('zero_hour_maintained', models.BooleanField(default=False)),
                ('assembly_arrangement', models.TextField(blank=True, null=True)),
                ('birthday_celebration', models.TextField(blank=True, null=True)),
                ('rollcall_primary_present', models.PositiveIntegerField(default=0)),
                ('rollcall_primary_total', models.PositiveIntegerField(default=0)),
                ('rollcall_primary_absent', models.PositiveIntegerField(default=0)),
                ('rollcall_high_school_present', models.PositiveIntegerField(default=0)),
                ('rollcall_high_school_total', models.PositiveIntegerField(default=0)),
                ('rollcall_high_school_absent', models.PositiveIntegerField(default=0)),
                ('rollcall_hr_sec_present', models.PositiveIntegerField(default=0)),
                ('rollcall_hr_sec_total', models.PositiveIntegerField(default=0)),
                ('rollcall_hr_sec_absent', models.PositiveIntegerField(default=0)),
                ('defaulters_uniform', models.CharField(blank=True, max_length=20, null=True)),
                ('defaulters_haircut', models.CharField(blank=True, max_length=20, null=True)),
                ('defaulters_nailcut', models.CharField(blank=True, max_length=20, null=True)),
                ('defaulters_shoes', models.CharField(blank=True, max_length=20, null=True)),
                ('defaulters_socks', models.CharField(blank=True, max_length=20, null=True)),
                ('defaulters_tie', models.CharField(blank=True, max_length=20, null=True)),
                ('defaulters_belt', models.CharField(blank=True, max_length=20, null=True)),
                ('defaulters_id_card', models.CharField(blank=True, max_length=20, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('school_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institutions.school')),
                ('report_submitted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staff.staff')),
            ],
            options={
                'ordering': ['-report_date'],
                'unique_together': {('school_name', 'report_date')},
            },
        ),
        migrations.CreateModel(
            name='MorningReportSubstaff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('reporting_time', models.CharField(blank=True, max_length=10, null=True)),
                ('status', models.CharField(choices=[('Closed', 'Closed'), ('Open', 'Open'), ('In-Progress', 'In-Progress'), ('Issue', 'Issue')], default='Closed', max_length=20)),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='substaffs', to='jacobreports.morningreport')),
            ],
        ),
    ]
