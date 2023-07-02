from django import forms
from .models import enquiry,students
from django.contrib.auth.forms import UserCreationForm
from setup.models import academicyr,sclass,section
from institutions.models import school

gender = [
    ('Male', 'Male'),
    ('Female','Female'),
    ('Transgender','Transgender')
]
communication = [
    ('News Paper','News Paper'),
    ('Internet','Internet'),
    ('Email','Email'),
    ('TV/Radio','TV/Radio'),
    ('Banners','Banners'),
    ('Friends','Friends'),
    ('Other','Other')
]
status = [
    ('Open','Open'),
    ('Pending','Pending'),
    ('Closed','Closed'),


]

stud_status = [
    ('Active','Active'),
    ('In-Active','In-Active'),
    ('Transfer','Transfer'),
]

releg = [
    ('Hindu','Hindu'),
    ('Christian','Christian'),
    ('Muslim','Muslim'),
    ('Sikh','Sikh'),
    ('Buddhist','Buddhist'),
    ('Jain','Jain'),

]

blood = [
    ('A+','A+'),
    ('A-','A-'),
    ('B+','B+'),
    ('B-','B-'),
    ('O+','O+'),
    ('O-','O-'),
    ('AB+','AB+'),
    ('AB-','AB-')
]




class add_enq_form(forms.ModelForm):
    class Meta:
        model = enquiry
        fields = '__all__'
        labels = {
            'enq_student':'Student Name',
            'enq_name': 'Enquirer Name',
            'enq_gender':'Gender',
            'enq_date':'Date',
            'enq_followup':'Next Follow-up Date',
            'enq_class' : 'Class',
            'enq_mob' : 'Contact No',
            'enq_altmob' : 'Alternate No',
            'enq_email' : 'Email',
            'enq_ref' : 'Referer Name',
            'enq_communication': ' How do you come to know about our school',
            'enq_det' : 'Detail',
            'enq_status' : 'Status'

        }
        widgets = {
            'enq_student': forms.TextInput(attrs={'class': 'form-control'}),
            'enq_name': forms.TextInput(attrs={'class': 'form-control'}),
            'enq_gender': forms.Select(choices=gender,attrs={'class':'form-control'}),
            'enq_date': forms.DateInput(attrs={'class': 'form-control','type':'date'}),
            'enq_followup': forms.DateInput(attrs={'class': 'form-control','type':'date'}),
            'enq_class': forms.Select(attrs={'class':'form-control'}),
            'enq_mob': forms.NumberInput(attrs={'class': 'form-control'}),
            'enq_altmob': forms.NumberInput(attrs={'class': 'form-control'}),
            'enq_email': forms.EmailInput(attrs={'class':'form-control'}),
            'enq_ref': forms.TextInput(attrs={'class': 'form-control'}),
            'enq_communication': forms.Select(choices=communication,attrs={'class':'form-control'}),
            'enq_det': forms.TextInput(attrs={'class': 'form-control'}),
            'enq_status':forms.Select(choices=status,attrs={'class':'form-control'}),
            'school_name': forms.HiddenInput(attrs={'class': 'form-control'}),
            'acad_year': forms.HiddenInput(attrs={'class': 'form-control'}),



        }

class add_studentsForm(forms.ModelForm):
    class Meta:
        model = students
        fields = '__all__'
        fields =  ('first_name','last_name','gender','dob_date','phone','email','address','admn_date','religion','caste','blood_group',
                   'father_name','mother_name','father_occupation','mother_occupation','roll_no','class_name',
                   'secs','school_student','admn_no','ac_year','student_status','student_photo','usernm',)

        # def __init__(self, *args, **kwargs):
        #     super().__init__(*args, **kwargs)
        #     self.fields['id_secs'].queryset = section.objects.none()
        #     if 'section_name' in self.data:
        #         try:
        #             section_id = int(self.data.get('section_name'))
        #             self.fields['section_name'].queryset = section.objects.filter(section_id=section_id).order_by(
        #                 'name')
        #         except(ValueError, TypeError):
        #             pass  # invalid input from the client; ignore and fallback to empty professioncategory queryset
        #     elif self.instance.pk:
        #         self.fields['section_name'].queryset = self.instance.profession.professioncategory_set.order_by('name')

        labels= {
            'first_name': 'First Name :',
            'last_name': ' Last Name :',
            'gender':'Gender:',
            'dob_date': 'Date of Birth :',
            'phone': 'Phone/Mobile No :',
            'email': 'Email :',
            'address': 'Address :',
            'admn_date': 'Admission Date :',
            'religion': 'Religion :',
            'caste': 'Caste :',
            'blood_group': 'Blood Group :',
            'father_name': "Father's Name :",
            'mother_name': "Mother's Name :",
            'father_occupation':"Father's Occupation :",
            'mother_occupation': "Mother's Occupation :",
            'roll_no': 'Roll_No :',
            'class_name': 'Class :',
            'secs': 'Section :',
            'school_student': 'School_id:',
            'ac_year':'Academic Year',
            'student_status':'status',
            'usernm':'username'


        }
        widgets ={
            'first_name': forms.TextInput(attrs={'class':'form-control','placeholder': ' First Name', 'style': 'width: 300px;'}),
            'last_name': forms.TextInput(attrs={'class':'form-control','placeholder': ' First Name','style': 'width: 300px;'}),
            'dob_date': forms.DateInput(attrs={'class': 'form-control','type':'date'}),
            'gender':forms.Select(choices=gender),
            'phone': forms.TextInput(attrs={'class':'form-control','placeholder': ' Moble/Phone No', 'style': 'width: 300px;'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'address': forms.Textarea(attrs={'class':'form-control','rows':4, 'cols':15}),
            'admn_date':forms.DateInput(attrs={'class': 'form-control','type':'date'}),
            'religion': forms.Select(choices=releg,attrs={'class':'form-control'}),
            'caste':forms.TextInput(attrs={'class':'form-control'}),
            'blood_group':forms.Select(choices=blood,attrs={'class':'form-control'}),
            'father_name':forms.TextInput(attrs={'class':'form-control'}),
            'mother_name':forms.TextInput(attrs={'class':'form-control'}),
            'father_occupation':forms.TextInput(attrs={'class':'form-control'}),
            'mother_occupation':forms.TextInput(attrs={'class':'form-control'}),
             'roll_no': forms.TextInput(attrs={'class':'form-control'}),
             'class_name':forms.Select(attrs={'class':'form-control'}),
             'secs':forms.Select(attrs={'class':'form-control'}),
             'ac_year':forms.Select(attrs={'class':'form-control'}),
             'school_student':forms.HiddenInput(),
              'student_status':forms.Select(choices=stud_status,attrs={'class':'form-control'}),
              'usernm':forms.TextInput(attrs={'class':'form-control'}),


        }


class trans_students(forms.ModelForm):
    class Meta:
        model = students
        fields = '__all__'
        fields =  ('first_name','last_name','dob_date','phone','email','address','admn_date','religion','caste','blood_group',
                   'father_name','mother_name','father_occupation','mother_occupation','roll_no','class_name',
                   'secs','school_student','admn_no','ac_year','student_status','student_photo','tc_date')

        # def __init__(self, *args, **kwargs):
        #     super().__init__(*args, **kwargs)
        #     self.fields['id_secs'].queryset = section.objects.none()
        #     if 'section_name' in self.data:
        #         try:
        #             section_id = int(self.data.get('section_name'))
        #             self.fields['section_name'].queryset = section.objects.filter(section_id=section_id).order_by(
        #                 'name')
        #         except(ValueError, TypeError):
        #             pass  # invalid input from the client; ignore and fallback to empty professioncategory queryset
        #     elif self.instance.pk:
        #         self.fields['section_name'].queryset = self.instance.profession.professioncategory_set.order_by('name')

        labels= {
            'first_name': 'First Name :',
            'last_name': ' Last Name :',
            'dob_date': 'Date of Birth :',
            'gender':'Gender',
            'phone': 'Phone/Mobile No :',
            'email': 'Email :',
            'address': 'Address :',
            'admn_date': 'Admission Date :',
            'religion': 'Religion :',
            'caste': 'Caste :',
            'blood_group': 'Blood Group :',
            'father_name': "Father's Name :",
            'mother_name': "Mother's Name :",
            'father_occupation':"Father's Occupation :",
            'mother_occupation': "Mother's Occupation :",
            'roll_no': 'Roll_No :',
            'class_name': 'Class :',
            'secs': 'Section :',
            'school_student': 'School_id:',
            'ac_year':'Academic Year',
            'student_status':'status',
            'tc_date':'Transfer Date',


        }
        widgets ={
            'first_name': forms.TextInput(attrs={'class':'form-control','placeholder': ' First Name', 'style': 'width: 300px;'}),
            'last_name': forms.TextInput(attrs={'class':'form-control','placeholder': ' First Name','style': 'width: 300px;'}),
            'dob_date': forms.SelectDateWidget(),
            'gender':forms.Select(choices=gender),
            'phone': forms.TextInput(attrs={'class':'form-control','placeholder': ' Moble/Phone No', 'style': 'width: 300px;'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'address': forms.TextInput(attrs={'class':'form-control'}),
            'admn_date':forms.SelectDateWidget(),
            'religion': forms.Select(choices=releg,attrs={'class':'form-control'}),
            'caste':forms.TextInput(attrs={'class':'form-control'}),
            'blood_group':forms.Select(choices=blood,attrs={'class':'form-control'}),
            'father_name':forms.TextInput(attrs={'class':'form-control'}),
            'mother_name':forms.TextInput(attrs={'class':'form-control'}),
            'father_occupation':forms.TextInput(attrs={'class':'form-control'}),
            'mother_occupation':forms.TextInput(attrs={'class':'form-control'}),
             'roll_no': forms.TextInput(attrs={'class':'form-control'}),
             'class_name':forms.Select(attrs={'class':'form-control'}),
             'secs':forms.Select(attrs={'class':'form-control'}),
             'ac_year':forms.Select(attrs={'class':'form-control'}),
             'school_student':forms.Select(attrs={'class':'form-control'}),
              'student_status':forms.Select(choices=stud_status,attrs={'class':'form-control'}),
             'tc_date':forms.SelectDateWidget(),



        }

