from django.utils.timezone import now
from datetime import datetime
from django import forms
from .models import DoctoralStudents, ComprehensiveExam, TOR, SubjectLoad, Loa, Promissory
from .models import MasteralStudents, MasteralComprehensiveExam, MasteralTOR, MasteralEvaluationOfGrades, MasteralSubjectLoad, MasteralLoa, MasteralPromissory
from .models import Faculty, FacultyTOR,Diploma,Faculty_Publication,Faculty_Teaching_Load,Faculty_Work_Load,Faculty_Course_Syllabus,Faculty_Curriculumn_Mapping,Faculty_Research_Presentation_Cert,Faculty_Awards
current_year = datetime.now().year
start_year = 1972

# Doctoral Model ###########################################################################################
class DoctoralStudentsForm(forms.ModelForm):
    class Meta:
        model = DoctoralStudents
        fields = [
            'student_id',
            'first_name',
            'last_name',
            'middle_name',
            'gender',
            'semesters',
            'school_year',
            'programs',
            'student_type',
            'profile_picture',
        ]
        

    # Generate the school year choices dynamically
    current_year = now().year
    start_year = 1972
    SCHOOL_YEAR_CHOICES = [
        (f"{year}-{year + 1}", f"{year}-{year + 1}") for year in range(start_year, current_year + 1)
    ]

 

    
    # Add custom widgets to form fields
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'oninput': 'capitalizeFirstLetter(event)',
        }),
        required=True
    )
    middle_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'oninput': 'capitalizeFirstLetter(event)',
        }),
        required=True
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'oninput': 'capitalizeFirstLetter(event)',
        }),
        required=True
    )
    
   
   


class ComprehensiveExamForm(forms.ModelForm):
    class Meta:
        model = ComprehensiveExam
        fields = ['file']  # Keep only the 'file' field

class TORForm(forms.ModelForm):
    class Meta:
        model = TOR
        fields = ['file']



class SubjectLoadForm(forms.ModelForm):
    class Meta:
        model = SubjectLoad
        fields = ['file']

class LoaForm(forms.ModelForm):
    class Meta:
        model = Loa
        fields = ['file']
        
class PromissoryForm(forms.ModelForm):
    class Meta:
        model = Promissory
        fields = ['file']
        
#Masteral Model #########################################################################################################
class MasteralStudentsForm(forms.ModelForm):
    # Define Meta to link the form with the MasteralStudents model
    class Meta:
        model = MasteralStudents
        fields = [
            'student_id',
            'first_name',
            'last_name',
            'middle_name',
            'gender',
            'semesters',
            'school_year',
            'programs',
            'student_type',
            'majors',
            'mprofile_picture',
        ]
    
    # Generate school year choices dynamically based on the current year
    current_year = now().year
    start_year = 1972
    SCHOOL_YEAR_CHOICES = [
        (f"{year}-{year + 1}", f"{year}-{year + 1}") for year in range(start_year, current_year + 1)
    ]
    

    # Add custom widgets to form fields
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'oninput': 'capitalizeFirstLetter(event)',
        }),
        required=True
    )
    middle_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'oninput': 'capitalizeFirstLetter(event)',
        }),
        required=True
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'oninput': 'capitalizeFirstLetter(event)',
        }),
        required=True
    )
    
    
class MasteralComprehensiveExamForm(forms.ModelForm):
    class Meta:
        model = MasteralComprehensiveExam
        fields = ['file']  # Keep only the 'file' field

class MasteralTORForm(forms.ModelForm):
    class Meta:
        model = MasteralTOR
        fields = ['file']

class MasteralEvaluationOfGradesForm(forms.ModelForm):
    class Meta:
        model = MasteralEvaluationOfGrades  
        fields = ['file']

class MasteralSubjectLoadForm(forms.ModelForm):
    class Meta:
        model = MasteralSubjectLoad
        fields = ['file']

class MasteralLoaForm(forms.ModelForm):
    class Meta:
        model = MasteralLoa
        fields = ['file']
        
class MasteralPromissoryForm(forms.ModelForm):
    class Meta:
        model = MasteralPromissory
        fields = ['file']
        
# Faculty Model#######################################################################
class FacultyForm(forms.ModelForm):
    # Define Meta to link the form with the MasteralStudents model
    class Meta:
        model = Faculty
        fields = [
            'faculty_id',
            'first_name',
            'last_name',
            'middle_name',
            'gender',
            'fprofile_picture',
            
        ]
    
   
    # Add custom widgets to form fields
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'oninput': 'capitalizeFirstLetter(event)',
        }),
        required=True
    )
    middle_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'oninput': 'capitalizeFirstLetter(event)',
        }),
        required=True
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'oninput': 'capitalizeFirstLetter(event)',
        }),
        required=True
    )
   
    

class FacultyTORForm(forms.ModelForm):
    class Meta:
        model = FacultyTOR
        fields = ['file']  # Keep only the 'file' field

class DiplomaForm(forms.ModelForm):
    class Meta:
        model = Diploma
        fields = ['file']

class Faculty_PublicationForm(forms.ModelForm):
    class Meta:
        model = Faculty_Publication  
        fields = ['file']

class Faculty_Teaching_LoadForm(forms.ModelForm):
    class Meta:
        model = Faculty_Teaching_Load
        fields = ['file']

class Faculty_Work_LoadForm(forms.ModelForm):
    class Meta:
        model = Faculty_Work_Load
        fields = ['file']
        
class Faculty_Course_SyllabusForm(forms.ModelForm):
    class Meta:
        model = Faculty_Course_Syllabus
        fields = ['file']
        
class Faculty_Curriculumn_MappingForm(forms.ModelForm):
    class Meta:
        model = Faculty_Curriculumn_Mapping
        fields = ['file']
        
        
class Faculty_Research_Presentation_CertForm(forms.ModelForm):
    class Meta:
        model = Faculty_Research_Presentation_Cert
        fields = ['file']
        

class Faculty_AwardsForm(forms.ModelForm):
    class Meta:
        model = Faculty_Awards
        fields = ['file']
        
class DoctoralStudentFilterForm(forms.Form):
    semesters = forms.ChoiceField(choices=DoctoralStudents.SEMESTER_CHOICES, required=False)
    programs = forms.ChoiceField(choices=DoctoralStudents.PROGRAMS_CHOICES, required=False)
    student_type = forms.ChoiceField(choices=DoctoralStudents.STUDENT_TYPE_CHOICES, required=False)
    school_year = forms.ChoiceField(choices=DoctoralStudents.SCHOOL_YEAR_CHOICES, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['semesters'].choices = [("", "Select Semester")] + DoctoralStudents.SEMESTER_CHOICES
        self.fields['programs'].choices = [("", "Select Program")] + DoctoralStudents.PROGRAMS_CHOICES
        self.fields['student_type'].choices = [("", "Select Student Type")] + DoctoralStudents.STUDENT_TYPE_CHOICES
        self.fields['school_year'].choices = [("", "Select School Year")] + DoctoralStudents.SCHOOL_YEAR_CHOICES
