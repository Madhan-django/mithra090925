import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('institutions', '0008_alter_school_regno'),
        ('setup', '0011_homework_time'),
        ('staff', '0006_staff_staff_type_alter_staff_salary'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('order', models.IntegerField(default=1)),
                ('cls', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setup.sclass')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institutions.school')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chapters', to='setup.subjects')),
            ],
            options={'ordering': ['order', 'name'], 'unique_together': {('name', 'subject', 'school')}},
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField()),
                ('question_type', models.CharField(choices=[('MCQ', 'Multiple Choice'), ('SHORT', 'Short Answer'), ('LONG', 'Long Answer'), ('FILL', 'Fill in the Blank'), ('TF', 'True / False'), ('MATCH', 'Match the Following')], max_length=10)),
                ('difficulty', models.CharField(choices=[('EASY', 'Easy'), ('MEDIUM', 'Medium'), ('HARD', 'Hard')], default='MEDIUM', max_length=10)),
                ('marks', models.PositiveIntegerField(default=1)),
                ('tags', models.CharField(blank=True, max_length=200)),
                ('image', models.ImageField(blank=True, null=True, upload_to='qbank/questions/')),
                ('is_approved', models.BooleanField(default=False)),
                ('usage_count', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('academic_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setup.academicyr')),
                ('chapter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='qbank.chapter')),
                ('cls', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setup.sclass')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='staff.staff')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institutions.school')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setup.subjects')),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='QuestionOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option_text', models.TextField()),
                ('is_correct', models.BooleanField(default=False)),
                ('order', models.PositiveIntegerField(default=0)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='qbank.question')),
            ],
            options={'ordering': ['order']},
        ),
        migrations.CreateModel(
            name='QuestionAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.TextField()),
                ('explanation', models.TextField(blank=True)),
                ('question', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='answer', to='qbank.question')),
            ],
        ),
        migrations.CreateModel(
            name='ExamBlueprint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('total_marks', models.PositiveIntegerField()),
                ('duration_mins', models.PositiveIntegerField(default=180)),
                ('instructions', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('cls', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setup.sclass')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='staff.staff')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institutions.school')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setup.subjects')),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='BlueprintSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_name', models.CharField(max_length=100)),
                ('question_type', models.CharField(choices=[('MCQ', 'Multiple Choice'), ('SHORT', 'Short Answer'), ('LONG', 'Long Answer'), ('FILL', 'Fill in the Blank'), ('TF', 'True / False'), ('MATCH', 'Match the Following')], max_length=10)),
                ('marks_per_question', models.PositiveIntegerField()),
                ('num_questions', models.PositiveIntegerField()),
                ('num_to_attempt', models.PositiveIntegerField(blank=True, null=True)),
                ('difficulty', models.CharField(blank=True, choices=[('EASY', 'Easy'), ('MEDIUM', 'Medium'), ('HARD', 'Hard')], max_length=10)),
                ('order', models.PositiveIntegerField(default=1)),
                ('blueprint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='qbank.examblueprint')),
            ],
            options={'ordering': ['order']},
        ),
        migrations.CreateModel(
            name='QuestionPaper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('exam_name', models.CharField(max_length=150)),
                ('total_marks', models.PositiveIntegerField()),
                ('duration_mins', models.PositiveIntegerField(default=180)),
                ('instructions', models.TextField(blank=True)),
                ('set_label', models.CharField(default='A', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_published', models.BooleanField(default=False)),
                ('academic_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setup.academicyr')),
                ('blueprint', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='qbank.examblueprint')),
                ('cls', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setup.sclass')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='staff.staff')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institutions.school')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setup.subjects')),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='PaperSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_name', models.CharField(max_length=100)),
                ('marks_per_question', models.PositiveIntegerField(default=1)),
                ('num_to_attempt', models.PositiveIntegerField(blank=True, null=True)),
                ('section_instructions', models.TextField(blank=True)),
                ('order', models.PositiveIntegerField(default=1)),
                ('paper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='qbank.questionpaper')),
            ],
            options={'ordering': ['order']},
        ),
        migrations.CreateModel(
            name='PaperQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(default=1)),
                ('paper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paper_questions', to='qbank.questionpaper')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qbank.question')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='qbank.papersection')),
            ],
            options={'ordering': ['order'], 'unique_together': {('paper', 'question')}},
        ),
    ]
