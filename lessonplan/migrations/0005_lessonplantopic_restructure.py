import django.db.models.deletion
from django.db import migrations, models


def migrate_topics(apps, schema_editor):
    LessonPlan      = apps.get_model('lessonplan', 'LessonPlan')
    LessonPlanTopic = apps.get_model('lessonplan', 'LessonPlanTopic')
    for plan in LessonPlan.objects.all():
        LessonPlanTopic.objects.create(
            lesson_plan      = plan,
            topic            = plan.topic,
            date             = plan.date,
            periods_required = plan.period_number,
            teaching_method  = plan.teaching_method,
            status           = plan.status,
            objectives       = plan.objectives,
            content_taught   = plan.content_taught,
        )


class Migration(migrations.Migration):

    dependencies = [
        ('lessonplan', '0004_remove_googledrivertoken'),
    ]

    operations = [
        # 1. Create the new topic model (keeping old fields on LessonPlan for data migration)
        migrations.CreateModel(
            name='LessonPlanTopic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=300)),
                ('date', models.DateField()),
                ('periods_required', models.PositiveSmallIntegerField(default=1)),
                ('teaching_method', models.CharField(
                    choices=[('Lecture','Lecture'),('Discussion','Discussion'),('Activity','Activity'),
                             ('Demo','Demonstration'),('Review','Review'),('Assessment','Assessment'),
                             ('Group Work','Group Work')],
                    default='Lecture', max_length=20)),
                ('status', models.CharField(
                    choices=[('Planned','Planned'),('Taught','Taught'),('Skipped','Skipped')],
                    default='Planned', max_length=10)),
                ('objectives', models.TextField(blank=True)),
                ('content_taught', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('lesson_plan', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='topics',
                    to='lessonplan.lessonplan',
                )),
            ],
            options={'ordering': ['date', 'id']},
        ),

        # 2. Migrate existing data
        migrations.RunPython(migrate_topics, migrations.RunPython.noop),

        # 3. Remove old topic-level fields from LessonPlan
        migrations.RemoveField(model_name='lessonplan', name='topic'),
        migrations.RemoveField(model_name='lessonplan', name='date'),
        migrations.RemoveField(model_name='lessonplan', name='period_number'),
        migrations.RemoveField(model_name='lessonplan', name='teaching_method'),
        migrations.RemoveField(model_name='lessonplan', name='status'),
        migrations.RemoveField(model_name='lessonplan', name='objectives'),
        migrations.RemoveField(model_name='lessonplan', name='content_taught'),

        # 4. Update ordering on LessonPlan
        migrations.AlterModelOptions(
            name='lessonplan',
            options={'ordering': ['cls', 'chapter']},
        ),
    ]
