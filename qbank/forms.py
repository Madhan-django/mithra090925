from django import forms
from .models import Question, ExamBlueprint, QuestionPaper, PaperSection, Chapter


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['cls', 'subject', 'chapter', 'question_type', 'difficulty',
                  'marks', 'tags', 'image', 'question_text', 'is_approved']
        widgets = {
            'question_text': forms.Textarea(attrs={'rows': 4}),
            'tags': forms.TextInput(attrs={'placeholder': 'e.g. algebra, chapter1'}),
        }


class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['name', 'subject', 'cls', 'order']


class ExamBlueprintForm(forms.ModelForm):
    class Meta:
        model = ExamBlueprint
        fields = ['name', 'cls', 'subject', 'total_marks', 'duration_mins', 'instructions']
        widgets = {
            'instructions': forms.Textarea(attrs={'rows': 3}),
        }


class QuestionPaperForm(forms.ModelForm):
    class Meta:
        model = QuestionPaper
        fields = ['title', 'cls', 'subject', 'exam_name', 'total_marks',
                  'duration_mins', 'set_label', 'instructions', 'blueprint']
        widgets = {
            'instructions': forms.Textarea(attrs={'rows': 3}),
        }


class PaperSectionForm(forms.ModelForm):
    class Meta:
        model = PaperSection
        fields = ['section_name', 'marks_per_question', 'num_to_attempt', 'section_instructions']
        widgets = {
            'section_instructions': forms.Textarea(attrs={'rows': 2}),
        }
