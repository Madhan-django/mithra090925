from django.contrib import admin
from .models import (Chapter, Question, QuestionOption, QuestionAnswer,
                     ExamBlueprint, BlueprintSection, QuestionPaper,
                     PaperSection, PaperQuestion)


class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption
    extra = 4


class QuestionAnswerInline(admin.StackedInline):
    model = QuestionAnswer
    extra = 1


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'subject', 'cls', 'question_type', 'difficulty', 'marks', 'is_approved']
    list_filter = ['question_type', 'difficulty', 'is_approved', 'school']
    search_fields = ['question_text', 'tags']
    inlines = [QuestionOptionInline, QuestionAnswerInline]


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'cls', 'school', 'order']


@admin.register(ExamBlueprint)
class ExamBlueprintAdmin(admin.ModelAdmin):
    list_display = ['name', 'cls', 'subject', 'total_marks', 'duration_mins']


@admin.register(QuestionPaper)
class QuestionPaperAdmin(admin.ModelAdmin):
    list_display = ['title', 'cls', 'subject', 'exam_name', 'total_marks', 'set_label', 'is_published']
