from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('examination', '0008_merge_20240702_1601'),
        ('institutions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GradeScale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_percent', models.DecimalField(decimal_places=2, max_digits=5)),
                ('max_percent', models.DecimalField(decimal_places=2, max_digits=5)),
                ('grade', models.CharField(max_length=5)),
                ('grade_point', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('remark', models.CharField(blank=True, max_length=50, null=True)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institutions.school')),
            ],
            options={
                'ordering': ['-min_percent'],
            },
        ),
    ]
