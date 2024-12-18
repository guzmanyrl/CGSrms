from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline, StackedInline  # Use Unfold's extensions
from django.utils.html import format_html

from .models import (
    DoctoralStudents, ComprehensiveExam, TOR, SubjectLoad, Loa, Promissory,
    MasteralStudents, MasteralComprehensiveExam, MasteralTOR, MasteralEvaluationOfGrades,
    MasteralSubjectLoad, MasteralLoa, MasteralPromissory, Faculty, FacultyTOR, Diploma,
    Faculty_Publication, Faculty_Teaching_Load, Faculty_Work_Load, Faculty_Course_Syllabus,
    Faculty_Curriculumn_Mapping, Faculty_Research_Presentation_Cert, Faculty_Awards
)

# Define a reusable method for file preview
class FilePreviewMixin:
    def file_preview(self, instance):
        if instance.file and instance.file.url:
            # Render an HTML img tag for images or provide a message for other files
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', instance.file.url)
        return "No preview available"
    file_preview.short_description = "Preview"

# Inline classes with file preview
class ComprehensiveExamInline(FilePreviewMixin, TabularInline):
    model = ComprehensiveExam
    extra = 1
    fields = ['file', 'file_preview']
    readonly_fields = ['file_preview']

class TORInline(FilePreviewMixin, TabularInline):
    model = TOR
    extra = 1
    fields = ['file', 'file_preview']
    readonly_fields = ['file_preview']

class SubjectLoadInline(FilePreviewMixin, TabularInline):
    model = SubjectLoad
    extra = 1
    fields = ['file', 'file_preview']
    readonly_fields = ['file_preview']

class LoaInline(FilePreviewMixin, TabularInline):
    model = Loa
    extra = 1
    fields = ['file', 'file_preview']
    readonly_fields = ['file_preview']

class PromissoryInline(FilePreviewMixin, TabularInline):
    model = Promissory
    extra = 1
    fields = ['file', 'file_preview']
    readonly_fields = ['file_preview']

# Register the DoctoralStudents model with Unfold
@admin.register(DoctoralStudents)
class DoctoralStudentsAdmin(ModelAdmin):  # Use Unfold's ModelAdmin
    list_display = ['first_name', 'last_name', 'student_id', 'school_year', 'programs']
    search_fields = ['first_name', 'last_name', 'student_id']
    list_filter = ['programs', 'school_year', 'gender']
    inlines = [ComprehensiveExamInline, TORInline, SubjectLoadInline, LoaInline, PromissoryInline]

# Masteral inlines
class MasteralComprehensiveExamInline(FilePreviewMixin, TabularInline):
    model = MasteralComprehensiveExam
    extra = 1
    fields = ['file', 'file_preview']
    readonly_fields = ['file_preview']

class MasteralTORInline(FilePreviewMixin, TabularInline):
    model = MasteralTOR
    extra = 1
    fields = ['file', 'file_preview']
    readonly_fields = ['file_preview']

class MasteralEvaluationOfGradesInline(FilePreviewMixin, TabularInline):
    model = MasteralEvaluationOfGrades
    extra = 1
    fields = ['file', 'file_preview']
    readonly_fields = ['file_preview']

class MasteralSubjectLoadInline(FilePreviewMixin, TabularInline):
    model = MasteralSubjectLoad
    extra = 1
    fields = ['file', 'file_preview']
    readonly_fields = ['file_preview']

class MasteralLoaInline(FilePreviewMixin, TabularInline):
    model = MasteralLoa
    extra = 1
    fields = ['file', 'file_preview']
    readonly_fields = ['file_preview']

class MasteralPromissoryInline(FilePreviewMixin, TabularInline):
    model = MasteralPromissory
    extra = 1
    fields = ['file', 'file_preview']
    readonly_fields = ['file_preview']

@admin.register(MasteralStudents)
class MasteralStudentsAdmin(ModelAdmin):
    list_display = ['first_name', 'last_name', 'student_id', 'school_year', 'programs']
    search_fields = ['first_name', 'last_name', 'student_id']
    list_filter = ['programs', 'majors', 'school_year', 'gender']
    inlines = [
        MasteralComprehensiveExamInline, MasteralTORInline, MasteralEvaluationOfGradesInline,
        MasteralSubjectLoadInline, MasteralLoaInline, MasteralPromissoryInline
    ]

# Faculty inlines
class FacultyTORInline(FilePreviewMixin, TabularInline):
    model = FacultyTOR
    extra = 1
    fields = ['file', 'file_preview']
    readonly_fields = ['file_preview']

class DiplomaInline(FilePreviewMixin, TabularInline):
    model = Diploma
    extra = 1
    fields = ['file', 'file_preview']
    readonly_fields = ['file_preview']

class Faculty_PublicationInline(FilePreviewMixin, TabularInline):
    model = Faculty_Publication
    extra = 1
    fields = ['file', 'file_preview']
    readonly_fields = ['file_preview']

class Faculty_Teaching_LoadInline(FilePreviewMixin, TabularInline):
    model = Faculty_Teaching_Load
    extra = 1
    fields = ['file', 'file_preview']
    readonly_fields = ['file_preview']

class Faculty_Work_LoadInline(FilePreviewMixin, TabularInline):
    model = Faculty_Work_Load
    extra = 1
    fields = ['file', 'file_preview']
    readonly_fields = ['file_preview']

class Faculty_Course_SyllabusInline(FilePreviewMixin, TabularInline):
    model = Faculty_Course_Syllabus
    extra = 1
    fields = ['file', 'file_preview']
    readonly_fields = ['file_preview']

class Faculty_Curriculumn_MappingInline(FilePreviewMixin, TabularInline):
    model = Faculty_Curriculumn_Mapping
    extra = 1
    fields = ['file', 'file_preview']
    readonly_fields = ['file_preview']

class Faculty_Research_Presentation_CertInline(FilePreviewMixin, TabularInline):
    model = Faculty_Research_Presentation_Cert
    extra = 1
    fields = ['file', 'file_preview']
    readonly_fields = ['file_preview']

class Faculty_AwardsInline(FilePreviewMixin, TabularInline):
    model = Faculty_Awards
    extra = 1
    fields = ['file', 'file_preview']
    readonly_fields = ['file_preview']

@admin.register(Faculty)
class FacultyAdmin(ModelAdmin):
    list_display = ['first_name', 'last_name', 'faculty_id', 'middle_name', 'gender']
    search_fields = ['first_name', 'last_name', 'faculty_id']
    list_filter = ['gender', 'middle_name']
    inlines = [
        FacultyTORInline, DiplomaInline, Faculty_PublicationInline, Faculty_Teaching_LoadInline,
        Faculty_Work_LoadInline, Faculty_Course_SyllabusInline, Faculty_Curriculumn_MappingInline,
        Faculty_Research_Presentation_CertInline, Faculty_AwardsInline
    ]
