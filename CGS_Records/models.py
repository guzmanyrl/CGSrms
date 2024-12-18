from django.db import models
from datetime import datetime
import os
from django.utils import timezone
current_year = datetime.now().year
start_year = 1972

# DoctoralStudents Model
class DoctoralStudents(models.Model):
    SEMESTER_CHOICES = [
        ('1st', '1st Semester'),
        ('2nd', '2nd Semester'),
        ('3rd', 'Summer')
    ]

    PROGRAMS_CHOICES = [
        ('PhD.  Education Major in Educational Management', 'PhD.  Education Major in Educational Management'),
        ('PhD. in Technology Management', 'PhD. in Technology Management'),
        ('Doctor of Management', 'Doctor of Management'),
    ]
    
    STUDENT_TYPE_CHOICES = [
        ('New', 'New'),
        ('Old', 'Old'),
       
    ]

    start_year = 1972
    current_year = datetime.now().year
    SCHOOL_YEAR_CHOICES = [
        (f"{year}-{year + 1}", f"{year}-{year + 1}") for year in range(start_year, current_year + 1)
    ]

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ]
    
    first_name = models.CharField(max_length=100, default='', blank=True)
    last_name = models.CharField(max_length=100, default='', blank=True)
    profile_picture = models.ImageField(upload_to='uploads/profile_pictures/', blank=True, null=True)
    middle_name = models.CharField(max_length=100, default='', blank=True)
    student_id = models.CharField(max_length=50, unique=True)
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES, default='', blank=True)
    semesters = models.CharField(max_length=100, choices=SEMESTER_CHOICES, blank=True)
    school_year = models.CharField(max_length=100, choices=SCHOOL_YEAR_CHOICES, blank=True)
    programs = models.CharField(max_length=50, choices=PROGRAMS_CHOICES, blank=True)
    
    student_type = models.CharField(max_length=100, choices=STUDENT_TYPE_CHOICES, blank=True)
   

    statistics_score = models.IntegerField(null=True, blank=True)
    philo_score = models.IntegerField(null=True, blank=True)
    research_score = models.IntegerField(null=True, blank=True)
    major_score = models.IntegerField(null=True, blank=True)
    remarks = models.CharField(max_length=100, null=True, blank=True)
    
    

    def __str__(self):
        return f"{self.first_name} {self.last_name}"




# Uploaded Files For DoctoralStudents---------------------------------------------------------------------------------------------
class ComprehensiveExam(models.Model):
    student = models.ForeignKey(DoctoralStudents, on_delete=models.CASCADE, related_name="comprehensive_exams")
    file = models.FileField(upload_to="uploads/comprehensive_exams/")
    uploaded_at = models.DateTimeField(default=timezone.now)
    file_size = models.CharField(max_length=20, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # Check if the file exists and calculate its size
        if self.file:
            size_in_bytes = self.file.size
            self.file_size = self.format_size(size_in_bytes)
        super().save(*args, **kwargs)  # Save the instance

    def format_size(self, size_in_bytes):
        # Convert bytes to a human-readable format (KB, MB, GB, etc.)
        for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if size_in_bytes < 1024.0:
                return f"{size_in_bytes:.2f} {unit}"
            size_in_bytes /= 1024.0
        return f"{size_in_bytes:.2f} PB"  # In case of very large files

    def __str__(self):
        return f"{self.file.name} ({self.file_size})"

class TOR(models.Model):
    student = models.ForeignKey(DoctoralStudents, on_delete=models.CASCADE, related_name="tor_files")
    file = models.FileField(upload_to="uploads/tor/")
    uploaded_at = models.DateTimeField(default=timezone.now)
    file_size = models.CharField(max_length=20, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # Check if the file exists and calculate its size
        if self.file:
            size_in_bytes = self.file.size
            self.file_size = self.format_size(size_in_bytes)
        super().save(*args, **kwargs)  # Save the instance

    def format_size(self, size_in_bytes):
        # Convert bytes to a human-readable format (KB, MB, GB, etc.)
        for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if size_in_bytes < 1024.0:
                return f"{size_in_bytes:.2f} {unit}"
            size_in_bytes /= 1024.0
        return f"{size_in_bytes:.2f} PB"  # In case of very large files

    def __str__(self):
        return f"{self.file.name} ({self.file_size})"


    
    def save(self, *args, **kwargs):
        # Check if the file exists and calculate its size
        if self.file:
            size_in_bytes = self.file.size
            self.file_size = self.format_size(size_in_bytes)
        super().save(*args, **kwargs)  # Save the instance

    def format_size(self, size_in_bytes):
        # Convert bytes to a human-readable format (KB, MB, GB, etc.)
        for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if size_in_bytes < 1024.0:
                return f"{size_in_bytes:.2f} {unit}"
            size_in_bytes /= 1024.0
        return f"{size_in_bytes:.2f} PB"  # In case of very large files

    def __str__(self):
        return f"{self.file.name} ({self.file_size})"
    
    
class SubjectLoad(models.Model):
    student = models.ForeignKey(DoctoralStudents, on_delete=models.CASCADE, related_name="subject_load")
    file = models.FileField(upload_to="uploads/subject_load/")
    uploaded_at = models.DateTimeField(default=timezone.now)
    file_size = models.CharField(max_length=20, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # Check if the file exists and calculate its size
        if self.file:
            size_in_bytes = self.file.size
            self.file_size = self.format_size(size_in_bytes)
        super().save(*args, **kwargs)  # Save the instance

    def format_size(self, size_in_bytes):
        # Convert bytes to a human-readable format (KB, MB, GB, etc.)
        for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if size_in_bytes < 1024.0:
                return f"{size_in_bytes:.2f} {unit}"
            size_in_bytes /= 1024.0
        return f"{size_in_bytes:.2f} PB"  # In case of very large files

    def __str__(self):
        return f"{self.file.name} ({self.file_size})"

class Loa(models.Model):
    student = models.ForeignKey(DoctoralStudents, on_delete=models.CASCADE, related_name="loa_files")
    file = models.FileField(upload_to="uploads/Loa/")
    uploaded_at = models.DateTimeField(default=timezone.now)
    file_size = models.CharField(max_length=20, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # Check if the file exists and calculate its size
        if self.file:
            size_in_bytes = self.file.size
            self.file_size = self.format_size(size_in_bytes)
        super().save(*args, **kwargs)  # Save the instance

    def format_size(self, size_in_bytes):
        # Convert bytes to a human-readable format (KB, MB, GB, etc.)
        for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if size_in_bytes < 1024.0:
                return f"{size_in_bytes:.2f} {unit}"
            size_in_bytes /= 1024.0
        return f"{size_in_bytes:.2f} PB"  # In case of very large files

    def __str__(self):
        return f"{self.file.name} ({self.file_size})"
    

class Promissory(models.Model):
    student = models.ForeignKey(DoctoralStudents, on_delete=models.CASCADE, related_name="promissory")
    file = models.FileField(upload_to="uploads/promissory_files/")
    uploaded_at = models.DateTimeField(default=timezone.now)
    file_size = models.CharField(max_length=20, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # Check if the file exists and calculate its size
        if self.file:
            size_in_bytes = self.file.size
            self.file_size = self.format_size(size_in_bytes)
        super().save(*args, **kwargs)  # Save the instance

    def format_size(self, size_in_bytes):
        # Convert bytes to a human-readable format (KB, MB, GB, etc.)
        for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if size_in_bytes < 1024.0:
                return f"{size_in_bytes:.2f} {unit}"
            size_in_bytes /= 1024.0
        return f"{size_in_bytes:.2f} PB"  # In case of very large files

    def __str__(self):
        return f"{self.file.name} ({self.file_size})"
#-----------------------------------------------------------------------------------------------------------------------

# Masteral Model--------------------------------------------------------------------------------------------------------
class MasteralStudents(models.Model):
    SEMESTER_CHOICES = [
        ('1st', '1st Semester'),
        ('2nd', '2nd Semester'),
        ('3rd', 'Summer'),
    ]

    PROGRAMS_CHOICES = [
        ('Master of Arts in Education', 'Master of Arts in Education'),
        ('Master of Management', 'Master of Management'),
    ]

    MAJORS_CHOICES = [
        ('Educational Management', 'Educational Management'),
        ('Elementary Education', 'Elementary Education'),
        ('Technology Education', 'Technology Education'),
        ('Home Economics', 'Home Economics'),
        ('Industrial Education', 'Industrial Education'),
        ('English', 'English'),
        ('Filipino', 'Filipino'),
        ('Physical Education', 'Physical Education'),
        ('Mathematics', 'Mathematics'),
        ('Marine Engineering & Nautical Science', 'Marine Engineering & Nautical Science'),
        ('Science', 'Science'),
    ]

    STUDENT_TYPE_CHOICES = [
        ('New', 'New'),
        ('Old', 'Old'),
    ]

    start_year = 1972
    current_year = datetime.now().year
    SCHOOL_YEAR_CHOICES = [
        (f"{year}-{year + 1}", f"{year}-{year + 1}") for year in range(start_year, current_year + 1)
    ]

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ]

    first_name = models.CharField(max_length=100, default='', blank=True)
    last_name = models.CharField(max_length=100, default='', blank=True)
    middle_name = models.CharField(max_length=100, default='', blank=True)
    student_id = models.CharField(max_length=50, unique=True)
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES, default='', blank=True)
    semesters = models.CharField(max_length=100, choices=SEMESTER_CHOICES, blank=True)
    school_year = models.CharField(max_length=100, choices=SCHOOL_YEAR_CHOICES, blank=True)
    programs = models.CharField(max_length=50, choices=PROGRAMS_CHOICES, blank=True)
    student_type = models.CharField(max_length=100, choices=STUDENT_TYPE_CHOICES, blank=True)
    majors = models.CharField(max_length=100, choices=MAJORS_CHOICES, blank=True)

    statistics_score = models.IntegerField(null=True, blank=True)
    philo_score = models.IntegerField(null=True, blank=True)
    research_score = models.IntegerField(null=True, blank=True)
    major_score = models.IntegerField(null=True, blank=True)
    remarks = models.CharField(max_length=100, null=True, blank=True)
    
    mprofile_picture = models.ImageField(upload_to='uploads/masteral_profile_pictures/', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Define file models for MasteralStudents
class MasteralComprehensiveExam(models.Model):
    student = models.ForeignKey(MasteralStudents, on_delete=models.CASCADE, related_name="masteral_comprehensive_exams")
    file = models.FileField(upload_to="uploads/masteral_comprehensive_exams/")
    uploaded_at = models.DateTimeField(default=timezone.now)
    file_size = models.CharField(max_length=20, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # Check if the file exists and calculate its size
        if self.file:
            size_in_bytes = self.file.size
            self.file_size = self.format_size(size_in_bytes)
        super().save(*args, **kwargs)  # Save the instance

    def format_size(self, size_in_bytes):
        # Convert bytes to a human-readable format (KB, MB, GB, etc.)
        for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if size_in_bytes < 1024.0:
                return f"{size_in_bytes:.2f} {unit}"
            size_in_bytes /= 1024.0
        return f"{size_in_bytes:.2f} PB"  # In case of very large files

    def __str__(self):
        return f"{self.file.name} ({self.file_size})"

class MasteralTOR(models.Model):
    student = models.ForeignKey(MasteralStudents, on_delete=models.CASCADE, related_name="masteral_tor_files")
    file = models.FileField(upload_to="uploads/masteral_tor/")
    uploaded_at = models.DateTimeField(default=timezone.now)
    file_size = models.CharField(max_length=20, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # Check if the file exists and calculate its size
        if self.file:
            size_in_bytes = self.file.size
            self.file_size = self.format_size(size_in_bytes)
        super().save(*args, **kwargs)  # Save the instance

    def format_size(self, size_in_bytes):
        # Convert bytes to a human-readable format (KB, MB, GB, etc.)
        for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if size_in_bytes < 1024.0:
                return f"{size_in_bytes:.2f} {unit}"
            size_in_bytes /= 1024.0
        return f"{size_in_bytes:.2f} PB"  # In case of very large files

    def __str__(self):
        return f"{self.file.name} ({self.file_size})"
    
    
class MasteralEvaluationOfGrades(models.Model):
    student = models.ForeignKey(MasteralStudents, on_delete=models.CASCADE, related_name="masteral_evaluation_grades")
    file = models.FileField(upload_to="uploads/masteral_evaluation_grades/")
    uploaded_at = models.DateTimeField(default=timezone.now)
    file_size = models.CharField(max_length=20, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # Check if the file exists and calculate its size
        if self.file:
            size_in_bytes = self.file.size
            self.file_size = self.format_size(size_in_bytes)
        super().save(*args, **kwargs)  # Save the instance

    def format_size(self, size_in_bytes):
        # Convert bytes to a human-readable format (KB, MB, GB, etc.)
        for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if size_in_bytes < 1024.0:
                return f"{size_in_bytes:.2f} {unit}"
            size_in_bytes /= 1024.0
        return f"{size_in_bytes:.2f} PB"  # In case of very large files

    def __str__(self):
        return f"{self.file.name} ({self.file_size})"

class MasteralSubjectLoad(models.Model):
    student = models.ForeignKey(MasteralStudents, on_delete=models.CASCADE, related_name="masteral_subject_load")
    file = models.FileField(upload_to="uploads/masteral_subject_load/")
    uploaded_at = models.DateTimeField(default=timezone.now)
    file_size = models.CharField(max_length=20, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # Check if the file exists and calculate its size
        if self.file:
            size_in_bytes = self.file.size
            self.file_size = self.format_size(size_in_bytes)
        super().save(*args, **kwargs)  # Save the instance

    def format_size(self, size_in_bytes):
        # Convert bytes to a human-readable format (KB, MB, GB, etc.)
        for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if size_in_bytes < 1024.0:
                return f"{size_in_bytes:.2f} {unit}"
            size_in_bytes /= 1024.0
        return f"{size_in_bytes:.2f} PB"  # In case of very large files

    def __str__(self):
        return f"{self.file.name} ({self.file_size})"

class MasteralLoa(models.Model):
    student = models.ForeignKey(MasteralStudents, on_delete=models.CASCADE, related_name="masteral_loa_files")
    file = models.FileField(upload_to="uploads/masteral_loa/")
    uploaded_at = models.DateTimeField(default=timezone.now)
    file_size = models.CharField(max_length=20, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # Check if the file exists and calculate its size
        if self.file:
            size_in_bytes = self.file.size
            self.file_size = self.format_size(size_in_bytes)
        super().save(*args, **kwargs)  # Save the instance

    def format_size(self, size_in_bytes):
        # Convert bytes to a human-readable format (KB, MB, GB, etc.)
        for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if size_in_bytes < 1024.0:
                return f"{size_in_bytes:.2f} {unit}"
            size_in_bytes /= 1024.0
        return f"{size_in_bytes:.2f} PB"  # In case of very large files

    def __str__(self):
        return f"{self.file.name} ({self.file_size})"
    

class MasteralPromissory(models.Model):
    student = models.ForeignKey(MasteralStudents, on_delete=models.CASCADE, related_name="masteral_promissory")
    file = models.FileField(upload_to="uploads/masteral_promissory_files/")
    uploaded_at = models.DateTimeField(default=timezone.now)
    file_size = models.CharField(max_length=20, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # Check if the file exists and calculate its size
        if self.file:
            size_in_bytes = self.file.size
            self.file_size = self.format_size(size_in_bytes)
        super().save(*args, **kwargs)  # Save the instance

    def format_size(self, size_in_bytes):
        # Convert bytes to a human-readable format (KB, MB, GB, etc.)
        for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if size_in_bytes < 1024.0:
                return f"{size_in_bytes:.2f} {unit}"
            size_in_bytes /= 1024.0
        return f"{size_in_bytes:.2f} PB"  # In case of very large files

    def __str__(self):
        return f"{self.file.name} ({self.file_size})"
    
#Faculty
class Faculty(models.Model):
    Gender_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    
    faculty_id = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100, default='', blank=True)
    last_name = models.CharField(max_length=100, default='', blank=True)
    middle_name = models.CharField(max_length=100, default='', blank=True)
    gender = models.CharField(max_length=100, choices=Gender_CHOICES, default='', blank=True)
    
    fprofile_picture = models.ImageField(upload_to='uploads/faculty_profile_pictures/', blank=True, null=True)
    
class FacultyTOR(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name="faculty_tor")
    file = models.FileField(upload_to="uploads/faculty_tor/")
    uploaded_at = models.DateTimeField(default=timezone.now)
    file_size = models.CharField(max_length=20, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # Check if the file exists and calculate its size
        if self.file:
            size_in_bytes = self.file.size
            self.file_size = self.format_size(size_in_bytes)
        super().save(*args, **kwargs)  # Save the instance

    def format_size(self, size_in_bytes):
        # Convert bytes to a human-readable format (KB, MB, GB, etc.)
        for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if size_in_bytes < 1024.0:
                return f"{size_in_bytes:.2f} {unit}"
            size_in_bytes /= 1024.0
        return f"{size_in_bytes:.2f} PB"  # In case of very large files

    def __str__(self):
        return f"{self.file.name} ({self.file_size})"

class Diploma(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name="faculty_diploma")
    file = models.FileField(upload_to="uploads/faculty_diploma/")
    uploaded_at = models.DateTimeField(default=timezone.now)
    file_size = models.CharField(max_length=20, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # Check if the file exists and calculate its size
        if self.file:
            size_in_bytes = self.file.size
            self.file_size = self.format_size(size_in_bytes)
        super().save(*args, **kwargs)  # Save the instance

    def format_size(self, size_in_bytes):
        # Convert bytes to a human-readable format (KB, MB, GB, etc.)
        for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if size_in_bytes < 1024.0:
                return f"{size_in_bytes:.2f} {unit}"
            size_in_bytes /= 1024.0
        return f"{size_in_bytes:.2f} PB"  # In case of very large files

    def __str__(self):
        return f"{self.file.name} ({self.file_size})"
    
    
class Faculty_Publication(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name="faculty_publication")
    file = models.FileField(upload_to="uploads/faculty_publication/")
    uploaded_at = models.DateTimeField(default=timezone.now)
    file_size = models.CharField(max_length=20, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # Check if the file exists and calculate its size
        if self.file:
            size_in_bytes = self.file.size
            self.file_size = self.format_size(size_in_bytes)
        super().save(*args, **kwargs)  # Save the instance

    def format_size(self, size_in_bytes):
        # Convert bytes to a human-readable format (KB, MB, GB, etc.)
        for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if size_in_bytes < 1024.0:
                return f"{size_in_bytes:.2f} {unit}"
            size_in_bytes /= 1024.0
        return f"{size_in_bytes:.2f} PB"  # In case of very large files

    def __str__(self):
        return f"{self.file.name} ({self.file_size})"

class Faculty_Teaching_Load(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name="faculty_teaching_load")
    file = models.FileField(upload_to="uploads/faculty_teaching_load/")
    uploaded_at = models.DateTimeField(default=timezone.now)
    file_size = models.CharField(max_length=20, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # Check if the file exists and calculate its size
        if self.file:
            size_in_bytes = self.file.size
            self.file_size = self.format_size(size_in_bytes)
        super().save(*args, **kwargs)  # Save the instance

    def format_size(self, size_in_bytes):
        # Convert bytes to a human-readable format (KB, MB, GB, etc.)
        for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if size_in_bytes < 1024.0:
                return f"{size_in_bytes:.2f} {unit}"
            size_in_bytes /= 1024.0
        return f"{size_in_bytes:.2f} PB"  # In case of very large files

    def __str__(self):
        return f"{self.file.name} ({self.file_size})"

class Faculty_Work_Load(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name="faculty_work_load")
    file = models.FileField(upload_to="uploads/faculty_work_load/")
    uploaded_at = models.DateTimeField(default=timezone.now)
    file_size = models.CharField(max_length=20, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # Check if the file exists and calculate its size
        if self.file:
            size_in_bytes = self.file.size
            self.file_size = self.format_size(size_in_bytes)
        super().save(*args, **kwargs)  # Save the instance

    def format_size(self, size_in_bytes):
        # Convert bytes to a human-readable format (KB, MB, GB, etc.)
        for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if size_in_bytes < 1024.0:
                return f"{size_in_bytes:.2f} {unit}"
            size_in_bytes /= 1024.0
        return f"{size_in_bytes:.2f} PB"  # In case of very large files

    def __str__(self):
        return f"{self.file.name} ({self.file_size})"
    

class Faculty_Course_Syllabus(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name="faculty_course_syllabus")
    file = models.FileField(upload_to="uploads/faculty_course_syllabus/")
    uploaded_at = models.DateTimeField(default=timezone.now)
    file_size = models.CharField(max_length=20, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # Check if the file exists and calculate its size
        if self.file:
            size_in_bytes = self.file.size
            self.file_size = self.format_size(size_in_bytes)
        super().save(*args, **kwargs)  # Save the instance

    def format_size(self, size_in_bytes):
        # Convert bytes to a human-readable format (KB, MB, GB, etc.)
        for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if size_in_bytes < 1024.0:
                return f"{size_in_bytes:.2f} {unit}"
            size_in_bytes /= 1024.0
        return f"{size_in_bytes:.2f} PB"  # In case of very large files

    def __str__(self):
        return f"{self.file.name} ({self.file_size})"
    

class Faculty_Curriculumn_Mapping(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name="faculty_curriculumn")
    file = models.FileField(upload_to="uploads/faculty_curriculumn/")
    uploaded_at = models.DateTimeField(default=timezone.now)
    file_size = models.CharField(max_length=20, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # Check if the file exists and calculate its size
        if self.file:
            size_in_bytes = self.file.size
            self.file_size = self.format_size(size_in_bytes)
        super().save(*args, **kwargs)  # Save the instance

    def format_size(self, size_in_bytes):
        # Convert bytes to a human-readable format (KB, MB, GB, etc.)
        for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if size_in_bytes < 1024.0:
                return f"{size_in_bytes:.2f} {unit}"
            size_in_bytes /= 1024.0
        return f"{size_in_bytes:.2f} PB"  # In case of very large files

    def __str__(self):
        return f"{self.file.name} ({self.file_size})"
    

class Faculty_Research_Presentation_Cert(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name="faculty_RPC")
    file = models.FileField(upload_to="uploads/faculty_RPC/")
    uploaded_at = models.DateTimeField(default=timezone.now)
    file_size = models.CharField(max_length=20, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # Check if the file exists and calculate its size
        if self.file:
            size_in_bytes = self.file.size
            self.file_size = self.format_size(size_in_bytes)
        super().save(*args, **kwargs)  # Save the instance

    def format_size(self, size_in_bytes):
        # Convert bytes to a human-readable format (KB, MB, GB, etc.)
        for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if size_in_bytes < 1024.0:
                return f"{size_in_bytes:.2f} {unit}"
            size_in_bytes /= 1024.0
        return f"{size_in_bytes:.2f} PB"  # In case of very large files

    def __str__(self):
        return f"{self.file.name} ({self.file_size})"
    
    
class Faculty_Awards(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name="faculty_awards")
    file = models.FileField(upload_to="uploads/faculty_awards/")
    uploaded_at = models.DateTimeField(default=timezone.now)
    file_size = models.CharField(max_length=20, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # Check if the file exists and calculate its size
        if self.file:
            size_in_bytes = self.file.size
            self.file_size = self.format_size(size_in_bytes)
        super().save(*args, **kwargs)  # Save the instance

    def format_size(self, size_in_bytes):
        # Convert bytes to a human-readable format (KB, MB, GB, etc.)
        for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if size_in_bytes < 1024.0:
                return f"{size_in_bytes:.2f} {unit}"
            size_in_bytes /= 1024.0
        return f"{size_in_bytes:.2f} PB"  # In case of very large files

    def __str__(self):
        return f"{self.file.name} ({self.file_size})"
    

