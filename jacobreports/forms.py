from django import forms
from .models import ClassTeacherReport


class ClassTeacherReportForm(forms.ModelForm):

    class Meta:
        model = ClassTeacherReport

        exclude = [
            'created_at'
        ]

        widgets = {

            # =========================
            # BASIC DETAILS
            # =========================

            'school_name': forms.Select(
               attrs={
                    'class': 'form-select',
                    'id': 'id_school_name'
                     }
               ),

            'report_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),

             'class_name': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_class_name'
            }),

            'section': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_section'
            }),



            'report_submitted_by': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            # =========================
            # NUMBER FIELDS
            # =========================

            'boys_on_roll': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 0
                }
            ),

            'girls_on_roll': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 0
                }
            ),

            'boys_present': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 0
                }
            ),

            'girls_present': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 0
                }
            ),

            'boys_uniform_defaulters': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 0
                }
            ),

            'girls_uniform_defaulters': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 0
                }
            ),

            'boys_absentees': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 0
                }
            ),

            'girls_absentees': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 0
                }
            ),

            # =========================
            # TEXTAREAS
            # =========================

            'action_taken': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3
                }
            ),

            'birthday_celebration': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 2
                }
            ),

            'accident_details': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 2
                }
            ),

            'defaulters': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 2
                }
            ),

            'homework_details': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 2
                }
            ),

            'drill_work_details': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 2
                }
            ),

            'activity_class': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 2
                }
            ),

            'announcements': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3
                }
            ),

            'teachers_remark': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3
                }
            ),

            'parents_remark': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3
                }
            ),

            'pupils_remark': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3
                }
            ),

            'meeting_details': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3
                }
            ),

            'suggestions_and_grievances': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3
                }
            ),

            # =========================
            # TRANSPORT DETAILS
            # =========================

            'private_auto_boys': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 0
                }
            ),

            'private_auto_girls': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 0
                }
            ),

            'cycle_boys': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 0
                }
            ),

            'cycle_girls': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 0
                }
            ),

            'walk_boys': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 0
                }
            ),

            'walk_girls': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 0
                }
            ),

            'school_van_boys': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 0
                }
            ),

            'school_van_girls': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 0
                }
            ),

            'bus_boys': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 0
                }
            ),

            'bus_girls': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 0
                }
            ),

            'others_boys': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 0
                }
            ),

            'others_girls': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 0
                }
            ),

        }