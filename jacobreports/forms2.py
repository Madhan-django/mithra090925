from django import forms
from .models import ClassTeacherReport, InchargeReport, ClassTeacherMapping


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


class InchargeReportForm(forms.ModelForm):

    class Meta:
        model = InchargeReport
        exclude = ['created_at']

        widgets = {

            # Basic Details
            'school_name': forms.Select(attrs={'class': 'form-select'}),
            'report_submitted_by': forms.Select(attrs={'class': 'form-select'}),
            'reporting_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'report_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-select'}),

            # Morning Session
            'late_comers_teachers': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'late_comers_duty_teachers': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'absentees_teachers': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'zero_hour_maintained': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'assembly_arrangements': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'class_teachers_morals': forms.Select(attrs={'class': 'form-select'}),
            'dispersing_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),

            # Lunch Break
            'ct_availability': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'children_without_lunch': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'lunch_atmosphere': forms.Select(attrs={'class': 'form-select'}),
            'noise_level': forms.Select(attrs={'class': 'form-select'}),

            # Afternoon Session
            'cram_conducted': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'special_class': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'activity_class': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'accident_details': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'incidents': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'pupils_detained': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),

            # Status Details
            'class_work_given': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'homework_corrected': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'handbook_checked': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'supervising_report': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),

            # Periods
            'period_1_time': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 8:00-8:45'}),
            'period_1': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'period_2_time': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 8:45-9:30'}),
            'period_2': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'period_3_time': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 9:30-10:15'}),
            'period_3': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'period_4_time': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 10:15-11:00'}),
            'period_4': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'period_5_time': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 12:00-12:45'}),
            'period_5': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'period_6_time': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 12:45-1:30'}),
            'period_6': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'period_7_time': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 1:30-2:15'}),
            'period_7': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'period_8_time': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2:15-3:00'}),
            'period_8': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),

            # Circular
            'circular_teachers': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'circular_parents': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'circular_pupils': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'circular_school': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),

            # Occurrences
            'birthday': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'competition_field_trip': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'celebration': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'meeting_conducted': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'meeting_details': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'demo_class': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),

            # Rounds & Prayer
            'rounds_report': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'staff_prayer_attendance': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),

            # Suggestions
            'suggestions_and_grievances': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),

            # Late Evening Class
            'late_evening_class': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),

            # Note
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),

            # Tomorrow's Assignment
            'tomorrows_assignment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class ClassTeacherMappingForm(forms.Form):
    from staff.models import staff as Staff

    incharge = forms.ModelChoiceField(
        queryset=Staff.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    class_teachers = forms.ModelMultipleChoiceField(
        queryset=Staff.objects.none(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select',
            'id': 'id_class_teachers',
        })
    )