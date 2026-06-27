from django.db import models
from institutions.models import school
from setup.models import sclass, subjects, academicyr
from staff.models import staff

QUESTION_TYPES = [
    ('MCQ', 'Multiple Choice'),
    ('SHORT', 'Short Answer'),
    ('LONG', 'Long Answer'),
    ('FILL', 'Fill in the Blank'),
    ('TF', 'True / False'),
    ('MATCH', 'Match the Following'),
]

DIFFICULTY = [
    ('EASY', 'Easy'),
    ('MEDIUM', 'Medium'),
    ('HARD', 'Hard'),
]


class Chapter(models.Model):
    name = models.CharField(max_length=150)
    subject = models.ForeignKey(subjects, on_delete=models.CASCADE, related_name='chapters')
    cls = models.ForeignKey(sclass, on_delete=models.CASCADE)
    school = models.ForeignKey(school, on_delete=models.CASCADE)
    order = models.IntegerField(default=1)

    class Meta:
        unique_together = ('name', 'subject', 'school')
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Question(models.Model):
    school = models.ForeignKey(school, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(academicyr, on_delete=models.CASCADE)
    cls = models.ForeignKey(sclass, on_delete=models.CASCADE)
    subject = models.ForeignKey(subjects, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True, blank=True)
    question_text = models.TextField()
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY, default='MEDIUM')
    marks = models.PositiveIntegerField(default=1)
    tags = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='qbank/questions/', blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    created_by = models.ForeignKey(staff, on_delete=models.SET_NULL, null=True, blank=True)
    usage_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.question_text[:80]


class QuestionOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    option_text = models.TextField()
    is_correct = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.option_text[:50]


class QuestionAnswer(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name='answer')
    answer_text = models.TextField()
    explanation = models.TextField(blank=True)

    def __str__(self):
        return f"Answer: {self.question}"


class ExamBlueprint(models.Model):
    name = models.CharField(max_length=200)
    school = models.ForeignKey(school, on_delete=models.CASCADE)
    cls = models.ForeignKey(sclass, on_delete=models.CASCADE)
    subject = models.ForeignKey(subjects, on_delete=models.CASCADE)
    total_marks = models.PositiveIntegerField()
    duration_mins = models.PositiveIntegerField(default=180)
    instructions = models.TextField(blank=True)
    created_by = models.ForeignKey(staff, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class BlueprintSection(models.Model):
    blueprint = models.ForeignKey(ExamBlueprint, on_delete=models.CASCADE, related_name='sections')
    section_name = models.CharField(max_length=100)
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES)
    marks_per_question = models.PositiveIntegerField()
    num_questions = models.PositiveIntegerField()
    num_to_attempt = models.PositiveIntegerField(null=True, blank=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY, blank=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.blueprint.name} – {self.section_name}"


class QuestionPaper(models.Model):
    title = models.CharField(max_length=200)
    school = models.ForeignKey(school, on_delete=models.CASCADE)
    cls = models.ForeignKey(sclass, on_delete=models.CASCADE)
    subject = models.ForeignKey(subjects, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(academicyr, on_delete=models.CASCADE)
    exam_name = models.CharField(max_length=150)
    total_marks = models.PositiveIntegerField()
    duration_mins = models.PositiveIntegerField(default=180)
    instructions = models.TextField(blank=True)
    set_label = models.CharField(max_length=10, default='A')
    blueprint = models.ForeignKey(ExamBlueprint, on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(staff, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} (Set {self.set_label})"


class PaperSection(models.Model):
    paper = models.ForeignKey(QuestionPaper, on_delete=models.CASCADE, related_name='sections')
    section_name = models.CharField(max_length=100)
    marks_per_question = models.PositiveIntegerField(default=1)
    num_to_attempt = models.PositiveIntegerField(null=True, blank=True)
    section_instructions = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.paper.title} – {self.section_name}"


class PaperQuestion(models.Model):
    paper = models.ForeignKey(QuestionPaper, on_delete=models.CASCADE, related_name='paper_questions')
    section = models.ForeignKey(PaperSection, on_delete=models.CASCADE, related_name='questions')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('paper', 'question')
        ordering = ['order']

    def __str__(self):
        return f"{self.paper.title} – Q{self.order}"
