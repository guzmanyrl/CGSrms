from django.shortcuts import render, get_object_or_404,redirect
from .models import  DoctoralStudents,ComprehensiveExam,TOR,Loa,SubjectLoad, Promissory
from .models import  MasteralStudents,MasteralComprehensiveExam,MasteralEvaluationOfGrades,MasteralTOR,MasteralLoa,MasteralSubjectLoad, MasteralPromissory
from .models import  Faculty,FacultyTOR,Diploma,Faculty_Publication,Faculty_Teaching_Load,Faculty_Work_Load,Faculty_Course_Syllabus,Faculty_Curriculumn_Mapping,Faculty_Research_Presentation_Cert,Faculty_Awards
from .forms import DoctoralStudentsForm, MasteralStudentsForm, FacultyForm
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
import json
import openpyxl
from datetime import datetime
from django.conf import settings
from django.http import HttpResponseNotAllowed
from django.http import JsonResponse
import logging
logger = logging.getLogger(__name__)
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
import mimetypes
import os
from django.db.models import Q
import pdfkit
config = pdfkit.configuration(wkhtmltopdf=settings.WKHTMLTOPDF_PATH)







logger = logging.getLogger(__name__)

# Create your views here.

@login_required(login_url='accounts:home_login')
def base (request):
    return render (request, 'base.html')


# Doctral Students adding
@login_required(login_url='accounts:home_login')
def doctoral(request):
    return render(request, 'CGS/doctoral.html')

@login_required(login_url='accounts:home_login')
def doctoral_evaluation(request):
    return render(request, 'CGS/doctoral_evaluation.html')

@login_required(login_url='accounts:home_login')
def doctoral_list(request):
    # Generate year range from 1972 to the current year
    start_year = 1972
    current_year = datetime.now().year
    year_range = range(start_year, current_year + 1)
    
    # Calculate year pairs (year, year+1) for school year options
    year_pairs = [(year, year + 1) for year in year_range]

    # Get filter parameters from the GET request
    student_type = request.GET.get('student_type', '')
    semesters = request.GET.get('semesters', '')
    programs = request.GET.get('programs', '')
    school_year = request.GET.get('school_year', '')

    # Start with all students
    students = DoctoralStudents.objects.all()

    # Apply filters if present in GET parameters
    if student_type:
        students = students.filter(student_type=student_type)
    if semesters:
        students = students.filter(semesters=semesters)
    if programs:
        students = students.filter(programs=programs)
   
    if school_year:
        students = students.filter(school_year=school_year)

    # Order the students alphabetically by last_name
    students = students.order_by('last_name', 'first_name')

    context = {
        'year_pairs': year_pairs,  # Pass the year pairs (year, year+1)
        'dstudent': students,
        'doctoral_program_choices': DoctoralStudents.PROGRAMS_CHOICES,
        'student_type_choices': DoctoralStudents.STUDENT_TYPE_CHOICES,
        'school_year_choices': DoctoralStudents.SCHOOL_YEAR_CHOICES,
        'current_year': current_year,
    }

    return render(request, 'CGS/doctoral_list.html', context)

    
# Function to handle multiple file uploads
def handle_file_upload(request, student, category):
    file_model = {
        'ComprehensiveExam': ComprehensiveExam,
        'TOR': TOR,
        'SubjectLoad': SubjectLoad,
        'Loa': Loa,
        'Promissory': Promissory,
        
    }[category]

    # Fetch files for this specific category (e.g., 'ComprehensiveExam_files')
    files = request.FILES.getlist(f"{category}_files")
    for file in files:
        file_instance = file_model(student=student, file=file)
        file_instance.save()

@login_required(login_url='accounts:home_login')
def add_doctoral_student(request):
    if request.method == "POST":
        form = DoctoralStudentsForm(request.POST)
        if form.is_valid():
            # Save the main student record
            dstudent = form.save()

            # Handle multiple file uploads for each file category
            for category in ['ComprehensiveExam', 'TOR', 'SubjectLoad', 'Loa','Promissory']:
                handle_file_upload(request, dstudent, category)

            # Success response with HTMX trigger
            return HttpResponse(
                status=204, 
                headers={'HX-Trigger': json.dumps({
                    "studentListChanged": None, 
                    "showMessage": f"{dstudent.first_name} {dstudent.last_name} added."
                })}
            )
    else:
        form = DoctoralStudentsForm()

    return render(request, 'CGS/doctoral_form.html', {'form': form})


@login_required(login_url='accounts:home_login')
def edit_doctoral_student(request, student_id):
    dstudent = get_object_or_404(DoctoralStudents, student_id=student_id)

    if request.method == "POST":
        form = DoctoralStudentsForm(request.POST, request.FILES, instance=dstudent)  # Handle files
        if form.is_valid():
            # If a new profile picture is uploaded, delete the old one
            if 'profile_picture' in request.FILES and dstudent.profile_picture:
                dstudent.profile_picture.delete(save=False)
            form.save()
            return HttpResponse(
                status=204,
                headers={'HX-Trigger': json.dumps({
                    "studentListChanged": None,
                    "showMessage": f"{dstudent.first_name} {dstudent.last_name} updated."
                })}
            )
    else:
        form = DoctoralStudentsForm(instance=dstudent)

    return render(request, 'CGS/edit_doctoral_form.html', {
        'form': form,
        'dstudent': dstudent
    })
    

@login_required(login_url='accounts:home_login')
def doctoral_update_profile_picture(request, student_id):
    dstudent = get_object_or_404(DoctoralStudents, student_id=student_id)

    if request.method == 'POST' and request.FILES.get('profile_picture'):
        # Delete the previous profile picture if it exists
        if dstudent.profile_picture and os.path.isfile(dstudent.profile_picture.path):
            os.remove(dstudent.profile_picture.path)

        # Save the new profile picture
        profile_picture = request.FILES['profile_picture']
        dstudent.profile_picture = profile_picture
        dstudent.save()

        return redirect('CGS_Records:manage_student_files', student_id=dstudent.student_id)
    
    return render(request, 'CGS/doctoral_student_files.html', {'dstudent': dstudent})




@login_required(login_url='accounts:home_login')
def remove_doctoral_student(request, student_id):
    dstudent = get_object_or_404(DoctoralStudents, student_id=student_id)

    # Define related file models
    related_models = [
        dstudent.comprehensive_exams.all(),
        dstudent.tor_files.all(),
        dstudent.subject_load.all(),
        dstudent.loa_files.all(),
        dstudent.promissory.all(),
    ]
    
    for related_files in related_models:
        for related_instance in related_files:
            # Delete the file from the filesystem before deleting the instance
            if related_instance.file:
                related_instance.file.delete(save=False)
            related_instance.delete()

    # Finally, delete the student record
    dstudent.delete()

    return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({"studentListChanged": None, "showMessage": "Student removed successfully."})})

@login_required(login_url='accounts:home_login')
def manage_student_files(request, student_id):
    dstudent = get_object_or_404(DoctoralStudents, student_id=student_id)

    # File extension categorization logic
    def get_file_extension(file_name):
        file_name = file_name.lower()
        if file_name.endswith('.pdf'):
            return 'pdf'
        elif file_name.endswith('.jpg') or file_name.endswith('.jpeg'):
            return 'image'
        elif file_name.endswith('.png'):
            return 'image'
        elif file_name.endswith('.doc') or file_name.endswith('.docx'):
            return 'document'
        else:
            return 'file'

    if request.method == "POST" and request.headers.get("HX-Request"):
        file_id = request.POST.get('file_id')
        file_category = request.POST.get('file_category')

        # Define the correct mapping here
        category_mapping = {
            'comprehensive_exams': dstudent.comprehensive_exams,
            'tor': dstudent.tor_files,
            'subject_load': dstudent.subject_load,
            'Loa': dstudent.loa_files,
            'promissory_files': dstudent.promissory,
        }

        # Check for valid category and delete the file
        if file_category in category_mapping:
            related_files = category_mapping[file_category].filter(id=file_id)
            if related_files.exists():
                related_file = related_files.first()
                if related_file.file:
                    related_file.file.delete(save=False)
                related_file.delete()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': "File not found."})

        return JsonResponse({'success': False, 'error': "Invalid file category."})

    # Render template with all files and their extensions
    existing_files = {
        'comprehensive_exams': dstudent.comprehensive_exams.all(),
        'tor': dstudent.tor_files.all(),
        'subject_load': dstudent.subject_load.all(),
        'Loa': dstudent.loa_files.all(),
        'promissory_files':dstudent.promissory.all(),
    }

    # Create a dictionary to hold file extensions
    file_extensions = {}

    # Loop through each category and fetch the file extension
    for category, files in existing_files.items():
        file_extensions[category] = []
        for file in files:
            file_extension = get_file_extension(file.file.name) if file.file else 'file'
            file_extensions[category].append(file_extension)

        # Ensure every category has a default empty list if no files exist
        if not file_extensions[category]:
            file_extensions[category] = []

    return render(request, 'CGS/doctoral_student_files.html', {
        'dstudent': dstudent,
        'existing_files': existing_files,
        'file_extensions': file_extensions,  # Pass the file extensions to the template
    })


@login_required(login_url='accounts:home_login')
def upload_files(request, student_id):
    # Ensure the student exists
    dstudent = get_object_or_404(DoctoralStudents, student_id=student_id)
    

    if request.method == "POST":
        # Get the uploaded files
        files = request.FILES.getlist('files[]')  # Get the list of uploaded files
        file_category = request.POST.get('file_category')

        if not file_category:
            return JsonResponse({"error": "File category is required."}, status=400)

        # Define a mapping of categories to the corresponding models
        category_mapping = {
            'comprehensive_exams': ComprehensiveExam,
            'tor': TOR,
            'subject_load': SubjectLoad,
            'Loa': Loa,
            'promissory_files':Promissory,
        }

        # Check for valid category and save the files
        if file_category in category_mapping:
            # Save the files
            for file in files:
                category_mapping[file_category].objects.create(student=dstudent, file=file)

            # Respond with success message
            return JsonResponse({"success": True, "message": "Files uploaded successfully."})

        # If the category is not valid, return an error
        return JsonResponse({"error": "Invalid file category."}, status=400)

    # If the method is not POST, return an error
    return JsonResponse({"error": "Invalid request method."}, status=400)


@login_required(login_url='accounts:home_login')
def view_file_inline(request, model_name, file_id):
    model_mapping = {
        'comprehensive_exam': ComprehensiveExam,
        'tor': TOR,
        'subject_load': SubjectLoad,
        'loa': Loa,
        'promissory_files': Promissory,
    }

    model = model_mapping.get(model_name.lower())
    if not model:
        raise Http404("Invalid model name.")

    file_instance = get_object_or_404(model, id=file_id)

  
    

    # Handle other MIME types for PDFs, images, etc.
    mime_type, _ = mimetypes.guess_type(file_instance.file.name)
    if mime_type and mime_type.startswith(('application/pdf', 'image/')):
        response = FileResponse(file_instance.file, content_type=mime_type)
        response['Content-Disposition'] = f'inline; filename="{file_instance.file.name}"'
        return response

    response = FileResponse(file_instance.file, as_attachment=True)
    response['Content-Disposition'] = f'attachment; filename="{file_instance.file.name}"'
    return response



#Masteral
@login_required(login_url='accounts:home_login')
def masteral (request):
    return render(request, 'CGS/masteral.html')

@login_required(login_url='accounts:home_login')
def masteral_list(request):
    start_year = 1972
    current_year = datetime.now().year
    year_range = range(start_year, current_year + 1)  # Generate the year range
    
    # Calculate year pairs (year, year+1) for school year options
    year_pairs = [(year, year + 1) for year in year_range]

    mstudents = MasteralStudents.objects.all().order_by('last_name', 'first_name', 'programs')

    # Apply filters if present in GET parameters
    programs = request.GET.get('programs')
    majors = request.GET.get('majors')
    student_type = request.GET.get('student_type')
    school_year = request.GET.get('school_year')

    if programs:
        mstudents = mstudents.filter(programs=programs)
    if majors:
        mstudents = mstudents.filter(majors=majors)
    if student_type:
        mstudents = mstudents.filter(student_type=student_type)
    if school_year:
        mstudents = mstudents.filter(school_year=school_year)

    context = {
        'year_pairs': year_pairs,  # Pass the year pairs (year, year+1)
        'mstudent': mstudents,
        'masteral_program_choices': MasteralStudents.PROGRAMS_CHOICES,
        'majors_choices': MasteralStudents.MAJORS_CHOICES,
        'student_type_choices': MasteralStudents.STUDENT_TYPE_CHOICES,
        'school_year_choices': MasteralStudents.SCHOOL_YEAR_CHOICES,
        'current_year': current_year,
    }
    return render(request, 'CGS/masteral_list.html', context)

    
@login_required(login_url='accounts:home_login')
def handle_masteral_file_upload(request, student, category):
    file_model = {
        'MasteralComprehensiveExam': MasteralComprehensiveExam,
        'MasteralTOR': MasteralTOR,
        'MasteralEvaluationOfGrades': MasteralEvaluationOfGrades,
        'MasteralSubjectLoad': MasteralSubjectLoad,
        'MasteralLoa': MasteralLoa,
        'MasteralPromissory': MasteralPromissory,
    }.get(category)

    files = request.FILES.getlist(f"{category}_files")
    if not files:
        logger.debug(f"No files found for category: {category}")
        return

    for file in files:
        logger.debug(f"Saving file for category: {category}, student: {student}, file name: {file.name}")
        file_instance = file_model(student=student, file=file)
        file_instance.save()
        
        
@login_required(login_url='accounts:home_login')
def add_masteral_student(request):
    if request.method == "POST":
        form = MasteralStudentsForm(request.POST, request.FILES)
        if form.is_valid():
            mstudent = form.save()  # Save MasteralStudent instance
            # Loop over file categories to upload related files
            for category in ['MasteralComprehensiveExam', 'MasteralTOR', 'MasteralEvaluationOfGrades', 'MasteralSubjectLoad', 'MasteralLoa','MasteralPromissory']:
                handle_masteral_file_upload(request, mstudent, category)

            return HttpResponse(
                status=204, 
                headers={'HX-Trigger': json.dumps({
                    "studentListChanged": None, 
                    "showMessage": f"{mstudent.first_name} {mstudent.last_name} added."
                })}
            )
    else:
        form = MasteralStudentsForm()

    return render(request, 'CGS/masteral_form.html', {'form': form})


@login_required(login_url='accounts:home_login')
def edit_masteral_student(request, student_id):
    mstudent = get_object_or_404(MasteralStudents, student_id=student_id)
    
    if request.method == "POST":
        form = MasteralStudentsForm(request.POST, instance=mstudent)
        
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={'HX-Trigger': json.dumps({
                    "studentListChanged": None,
                    "showMessage": f"{mstudent.first_name} {mstudent.last_name} updated."
                })}
            )
    else:
        form = MasteralStudentsForm(instance=mstudent)

    return render(request, 'CGS/edit_masteral_form.html', {
        'form': form,
        'mstudent': mstudent
    })
    

@login_required(login_url='accounts:home_login')
def masteral_update_profile_picture(request, student_id):
    mstudent = get_object_or_404(MasteralStudents, student_id=student_id)

    if request.method == 'POST' and request.FILES.get('mprofile_picture'):
        # Delete the previous profile picture if it exists
        if mstudent.mprofile_picture and os.path.isfile(mstudent.mprofile_picture.path):
            os.remove(mstudent.mprofile_picture.path)

        # Save the new profile picture
        mprofile_picture = request.FILES['mprofile_picture']
        mstudent.mprofile_picture = mprofile_picture
        mstudent.save()
        
        return redirect('CGS_Records:manage_masteral_student_files', student_id=mstudent.student_id)
    return render(request, 'CGS/masteral_student_files.html', {'mstudent': mstudent})


@login_required(login_url='accounts:home_login')
def remove_masteral_student(request, student_id):
    mstudent = get_object_or_404(MasteralStudents, student_id=student_id)

    # Define related file models for masteral student
    related_models = [
        mstudent.masteral_comprehensive_exams.all(),
        mstudent.masteral_tor_files.all(),
        mstudent.masteral_evaluation_grades.all(),
        mstudent.masteral_subject_load.all(),
        mstudent.masteral_loa_files.all(),
        mstudent.masteral_promissory.all(),
    ]
    
    for related_files in related_models:
        for related_instance in related_files:
            # Delete the file from the filesystem before deleting the instance
            if related_instance.file:
                related_instance.file.delete(save=False)
            related_instance.delete()

    # Finally, delete the student record
    mstudent.delete()

    return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({"studentListChanged": None, "showMessage": "Student removed successfully."})})


@login_required(login_url='accounts:home_login')
def manage_masteral_student_files(request, student_id):
    mstudent = get_object_or_404(MasteralStudents, student_id=student_id)

    # File extension categorization logic
    def get_file_extension(file_name):
        file_name = file_name.lower()
        if file_name.endswith('.pdf'):
            return 'pdf'
        elif file_name.endswith('.jpg') or file_name.endswith('.jpeg'):
            return 'image'
        elif file_name.endswith('.png'):
            return 'image'
        elif file_name.endswith('.doc') or file_name.endswith('.docx'):
            return 'document'
        else:
            return 'file'

    if request.method == "POST" and request.headers.get("HX-Request"):
        file_id = request.POST.get('file_id')
        file_category = request.POST.get('file_category')

        # Define the correct mapping here
        category_mapping = {
            'masteral_comprehensive_exams': mstudent.masteral_comprehensive_exams,
            'masteral_tor': mstudent.masteral_tor_files,
            'masteral_evaluation_of_grades': mstudent.masteral_evaluation_grades,
            'masteral_subject_load': mstudent.masteral_subject_load,
            'masteral_loa': mstudent.masteral_loa_files,
            'masteral_promissory_files': mstudent.masteral_promissory,
        }

        if file_category in category_mapping:
            related_files = category_mapping[file_category].filter(id=file_id)
            if related_files.exists():
                related_file = related_files.first()
                if related_file.file:
                    related_file.file.delete(save=False)
                related_file.delete()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': "File not found."})

        return JsonResponse({'success': False, 'error': "Invalid file category."})

    # Get all files and their extensions
    existing_files = {
        'masteral_comprehensive_exams': mstudent.masteral_comprehensive_exams.all(),
        'masteral_tor': mstudent.masteral_tor_files.all(),
        'masteral_evaluation_of_grades': mstudent.masteral_evaluation_grades.all(),
        'masteral_subject_load': mstudent.masteral_subject_load.all(),
        'masteral_loa': mstudent.masteral_loa_files.all(),
        'masteral_promissory_files': mstudent.masteral_promissory.all(),
    }

    # Create a dictionary to hold file extensions
    file_extensions = {}

    # Loop through each category and fetch the file extension
    for category, files in existing_files.items():
        file_extensions[category] = []
        for file in files:
            file_extension = get_file_extension(file.file.name) if file.file else 'file'
            file_extensions[category].append(file_extension)

        # Ensure every category has a default empty list if no files exist
        if not file_extensions[category]:
            file_extensions[category] = []

    return render(request, 'CGS/masteral_student_files.html', {
        'mstudent': mstudent,
        'existing_files': existing_files,
        'file_extensions': file_extensions,  # Pass the file extensions to the template
    })


    

@login_required(login_url='accounts:home_login')
def upload_masteral_files(request, student_id):
    mstudent = get_object_or_404(MasteralStudents, student_id=student_id)

    if request.method == "POST":
        files = request.FILES.getlist('files[]')
        file_category = request.POST.get('file_category')

        if not file_category:
            return JsonResponse({"error": "File category is required."}, status=400)

        category_mapping = {
            'masteral_comprehensive_exams': MasteralComprehensiveExam,
            'masteral_tor': MasteralTOR,
            'masteral_evaluation_of_grades': MasteralEvaluationOfGrades,
            'masteral_subject_load': MasteralSubjectLoad,
            'masteral_loa': MasteralLoa,
            'masteral_promissory_files': MasteralPromissory,
        }

        if file_category in category_mapping:
            for file in files:
                category_mapping[file_category].objects.create(student=mstudent, file=file)

            return JsonResponse({"success": True, "message": "Files uploaded successfully."})

        return JsonResponse({"error": "Invalid file category."}, status=400)

    return JsonResponse({"error": "Invalid request method."}, status=400)


@login_required(login_url='accounts:home_login')
def view_masteral_file_inline(request, model_name, file_id):
    # Mapping model names to model classes
    model_mapping = {
        'masteral_comprehensive_exam': MasteralComprehensiveExam,
        'masteral_tor': MasteralTOR,
        'masteral_evaluation_of_grades': MasteralEvaluationOfGrades,
        'masteral_subject_load': MasteralSubjectLoad,
        'masteral_loa': MasteralLoa,
        'masteral_promissory_files': MasteralPromissory,
    }

    # Get the appropriate model class
    model = model_mapping.get(model_name.lower())
    if model is None:
        raise Http404("Model not found.")

    # Retrieve the file instance based on file_id
    try:
        file_instance = model.objects.get(id=file_id)
    except model.DoesNotExist:
        raise Http404("File not found.")

    # Get the file's MIME type based on the file extension
    file_extension = file_instance.file.name.split('.')[-1].lower()
    mime_type, _ = mimetypes.guess_type(file_instance.file.name)
    
    if mime_type is None:
        mime_type = 'application/octet-stream'

    # If the file is a PDF, image, or Word document (.doc/.docx), try to open it inline
    if file_extension in ['pdf', 'jpg', 'jpeg', 'png', 'gif', 'bmp']:
        response = FileResponse(file_instance.file, content_type=mime_type)
        response['Content-Disposition'] = f'inline; filename="{file_instance.file.name}"'
    
    elif file_extension in ['doc', 'docx']:
        # For local testing, return the file directly or show it in an external viewer
        if settings.DEBUG:
            response = FileResponse(file_instance.file, content_type=mime_type)
            response['Content-Disposition'] = f'inline; filename="{file_instance.file.name}"'
        else:
            # For production, redirect to Google Docs Viewer (after uploading to a public server)
            google_docs_viewer_url = f'https://docs.google.com/viewer?url={request.build_absolute_uri(file_instance.file.url)}'
            return redirect(google_docs_viewer_url)

    # For other file types, default to download behavior
    else:
        response = FileResponse(file_instance.file, as_attachment=True)
        response['Content-Disposition'] = f'attachment; filename="{file_instance.file.name}"'
    
    return response


#Faculty views Functions
@login_required(login_url='accounts:home_login')
def faculty (request):
    return render (request, 'CGS/faculty.html')

@login_required(login_url='accounts:home_login')
def faculty_list(request):
    return render(request, 'CGS/faculty_list.html', {
        'faculty': Faculty.objects.all(),
    })

@login_required(login_url='accounts:home_login')
def handle_faculty_file_upload(request, faculty, category):
    file_model = {
        'FacultyTOR': FacultyTOR,
        'Diploma': Diploma,
        'Faculty_Publication': Faculty_Publication,
        'Faculty_Teaching_Load': Faculty_Teaching_Load,
        'Faculty_Work_Load': Faculty_Work_Load,
        'Faculty_Course_Syllabus': Faculty_Course_Syllabus,
        'Faculty_Curriculumn_Mapping':Faculty_Curriculumn_Mapping,
        'Faculty_Research_Presentation_Cert': Faculty_Research_Presentation_Cert,
        'Faculty_Awards': Faculty_Awards
    }.get(category)

    files = request.FILES.getlist(f"{category}_files")
    if not files:
        logger.debug(f"No files found for category: {category}")
        return

    for file in files:
        logger.debug(f"Saving file for category: {category}, faculty: {faculty}, file name: {file.name}")
        file_instance = file_model(faculty=faculty, file=file)
        file_instance.save()

@login_required(login_url='accounts:home_login')
def add_faculty(request):
    if request.method == "POST":
        form = FacultyForm(request.POST, request.FILES)
        if form.is_valid():
            faculty = form.save()

            # Loop over categories to handle file uploads
            for category in ['FacultyTOR', 'Diploma', 'Faculty_Publication', 'Faculty_Teaching_Load', 'Faculty_Work_Load','Faculty_Course_Syllabus','Faculty_Curriculumn_Mapping', 'Faculty_Research_Presentation_Cert', 'Faculty_Awards']:
                handle_faculty_file_upload(request, faculty, category)

            return HttpResponse(
                status=204,
                headers={'HX-Trigger': json.dumps({
                    "facultyListChanged": None, 
                    "showMessage": f"{faculty.first_name} {faculty.last_name} added."
                })}
            )
    else:
        form = FacultyForm()

    return render(request, 'CGS/faculty_form.html', {'form': form})


@login_required(login_url='accounts:home_login')
def edit_faculty(request, faculty_id):
    faculty = get_object_or_404(Faculty, faculty_id=faculty_id)
    
    if request.method == "POST":
        form = FacultyForm(request.POST, instance=faculty)
        
        if form.is_valid():
            form.save()
            # Only handle student details, not files here
            return HttpResponse(
                status=204,
                headers={'HX-Trigger': json.dumps({
                    "facultyListChanged": None,
                    "showMessage": f"{faculty.first_name} {faculty.last_name} updated."
                })}
            )
    else:
        form = FacultyForm(instance=faculty)

    return render(request, 'CGS/edit_faculty_form.html', {
        'form': form,
        'faculty': faculty
    })
    
    
@login_required(login_url='accounts:home_login')
def faculty_update_profile_picture(request, faculty_id):
    faculty = get_object_or_404(Faculty, faculty_id=faculty_id)

    if request.method == 'POST' and request.FILES.get('fprofile_picture'):
        # Delete the previous profile picture if it exists
        if faculty.fprofile_picture and os.path.isfile(faculty.fprofile_picture.path):
            os.remove(faculty.fprofile_picture.path)

        # Save the new profile picture
        fprofile_picture = request.FILES['fprofile_picture']
        faculty.fprofile_picture = fprofile_picture
        faculty.save()

        return redirect('CGS_Records:manage_faculty_files', faculty_id=faculty.faculty_id)
    return render(request, 'CGS/faculty_files.html', {'faculty': faculty})


@login_required(login_url='accounts:home_login')
def remove_faculty(request, faculty_id):
    faculty = get_object_or_404(Faculty, faculty_id=faculty_id)

    # Define related file models for masteral student
    related_models = [
        faculty.faculty_tor.all(),
        faculty.faculty_diploma.all(),
        faculty.faculty_publication.all(),
        faculty.faculty_teaching_load.all(),
        faculty.faculty_work_load.all(),
        faculty.faculty_course_syllabus.all(),
        faculty.faculty_curriculumn.all(),
        faculty.faculty_RPC.all(),
        faculty.faculty_awards.all(),
    ]
    
    for related_files in related_models:
        for related_instance in related_files:
            # Delete the file from the filesystem before deleting the instance
            if related_instance.file:
                related_instance.file.delete(save=False)
            related_instance.delete()

    # Finally, delete the student record
    faculty.delete()

    return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({"facultyListChanged": None, "showMessage": "Faculty member removed successfully."})})


@login_required(login_url='accounts:home_login')
def manage_faculty_files(request, faculty_id):
    faculty = get_object_or_404(Faculty, faculty_id=faculty_id)

    # File extension categorization logic
    def get_file_extension(file_name):
        file_name = file_name.lower()
        if file_name.endswith('.pdf'):
            return 'pdf'
        elif file_name.endswith('.jpg') or file_name.endswith('.jpeg'):
            return 'image'
        elif file_name.endswith('.png'):
            return 'image'
        elif file_name.endswith('.doc') or file_name.endswith('.docx'):
            return 'document'
        else:
            return 'file'

    if request.method == "POST" and request.headers.get("HX-Request"):
        file_id = request.POST.get('file_id')
        file_category = request.POST.get('file_category')

        # Define the correct mapping here
        category_mapping = {
            'faculty_tor': faculty.faculty_tor,
            'faculty_diploma': faculty.faculty_diploma,
            'faculty_publication': faculty.faculty_publication,
            'faculty_teaching_load': faculty.faculty_teaching_load,
            'faculty_work_load': faculty.faculty_work_load,
            'faculty_course_syllabus': faculty.faculty_course_syllabus,
            'faculty_curriculumn':faculty.faculty_curriculumn,
            'faculty_RPC': faculty.faculty_RPC,
            'faculty_awards': faculty.faculty_awards
        }

        if file_category in category_mapping:
            related_files = category_mapping[file_category].filter(id=file_id)
            if related_files.exists():
                related_file = related_files.first()
                if related_file.file:
                    related_file.file.delete(save=False)
                related_file.delete()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': "File not found."})

        return JsonResponse({'success': False, 'error': "Invalid file category."})

    # Get all files and their extensions
    existing_files = {
        'faculty_tor': faculty.faculty_tor.all(),
        'faculty_diploma': faculty.faculty_diploma.all(),
        'faculty_publication': faculty.faculty_publication.all(),
        'faculty_teaching_load': faculty.faculty_teaching_load.all(),
        'faculty_work_load': faculty.faculty_work_load.all(),
        'faculty_course_syllabus': faculty.faculty_course_syllabus.all(),
        'faculty_curriculumn':faculty.faculty_curriculumn.all(),
        'faculty_RPC': faculty.faculty_RPC.all(),
        'faculty_awards': faculty.faculty_awards.all()
    }

    # Create a dictionary to hold file extensions
    file_extensions = {}

    # Loop through each category and fetch the file extension
    for category, files in existing_files.items():
        file_extensions[category] = []
        for file in files:
            file_extension = get_file_extension(file.file.name) if file.file else 'file'
            file_extensions[category].append(file_extension)

        # Ensure every category has a default empty list if no files exist
        if not file_extensions[category]:
            file_extensions[category] = []

    return render(request, 'CGS/faculty_files.html', {
        'faculty': faculty,
        'existing_files': existing_files,
        'file_extensions': file_extensions,  # Pass the file extensions to the template
    })


    

@login_required(login_url='accounts:home_login')
def upload_faculty_files(request, faculty_id):
    # Fetch the Faculty instance based on the faculty_id
    faculty = get_object_or_404(Faculty, faculty_id=faculty_id)

    if request.method == "POST":
        # Get the list of files and the category from the POST request
        files = request.FILES.getlist('files[]')
        file_category = request.POST.get('file_category')

        # Ensure a file category is provided
        if not file_category:
            return JsonResponse({"error": "File category is required."}, status=400)

        # Mapping of file categories to the appropriate model
        category_mapping = {
            'faculty_tor': FacultyTOR,
            'faculty_diploma': Diploma,
            'faculty_publication': Faculty_Publication,
            'faculty_teaching_load': Faculty_Teaching_Load,
            'faculty_work_load': Faculty_Work_Load,
            'faculty_course_syllabus': Faculty_Course_Syllabus,
            'faculty_curriculumn':Faculty_Curriculumn_Mapping,
            'faculty_RPC': Faculty_Research_Presentation_Cert,
            'faculty_awards': Faculty_Awards,
        }

        # Check if the provided category is valid and handle the file upload
        if file_category in category_mapping:
            model_class = category_mapping[file_category]
            for file in files:
                # Create the corresponding instance for each file and save it
                model_class.objects.create(faculty=faculty, file=file)

            # Return a success response once files are uploaded
            return JsonResponse({"success": True, "message": "Files uploaded successfully."})

        # If the category is invalid, return an error response
        return JsonResponse({"error": "Invalid file category."}, status=400)

    # Return an error if the request method is not POST
    return JsonResponse({"error": "Invalid request method."}, status=400)


@login_required(login_url='accounts:home_login')
def view_faculty_file_inline(request, model_name, file_id):
    # Mapping model names to model classes
    model_mapping = {
        'faculty_tor': FacultyTOR,
        'faculty_diploma': Diploma,
        'faculty_publication': Faculty_Publication,
        'faculty_teaching_load': Faculty_Teaching_Load,
        'faculty_work_load': Faculty_Work_Load,
        'faculty_course_syllabus': Faculty_Course_Syllabus,
        'faculty_curriculumn':Faculty_Curriculumn_Mapping,
        'faculty_RPC': Faculty_Research_Presentation_Cert,
        'faculty_awards': Faculty_Awards
    }

    # Get the appropriate model class based on the model_name parameter
    model = model_mapping.get(model_name.lower())
    if model is None:
        raise Http404("Model not found.")

    # Retrieve the file instance based on file_id
    try:
        file_instance = model.objects.get(id=file_id)
    except model.DoesNotExist:
        raise Http404("File not found.")

    # Get the file's MIME type based on the file extension
    file_extension = file_instance.file.name.split('.')[-1].lower()
    mime_type, _ = mimetypes.guess_type(file_instance.file.name)

    # Set default MIME type if none is found
    if mime_type is None:
        mime_type = 'application/octet-stream'

    # If the file is a PDF, image, or Word document (.doc/.docx), try to open it inline
    if file_extension in ['pdf', 'jpg', 'jpeg', 'png', 'gif', 'bmp']:
        response = FileResponse(file_instance.file, content_type=mime_type)
        response['Content-Disposition'] = f'inline; filename="{file_instance.file.name}"'
    
    elif file_extension in ['doc', 'docx']:
        # For local testing, return the file directly or show it in an external viewer
        if settings.DEBUG:
            response = FileResponse(file_instance.file, content_type=mime_type)
            response['Content-Disposition'] = f'inline; filename="{file_instance.file.name}"'
        else:
            # For production, redirect to Google Docs Viewer (after uploading to a public server)
            google_docs_viewer_url = f'https://docs.google.com/viewer?url={request.build_absolute_uri(file_instance.file.url)}'
            return redirect(google_docs_viewer_url)

    # For other file types, default to download behavior
    else:
        response = FileResponse(file_instance.file, as_attachment=True)
        response['Content-Disposition'] = f'attachment; filename="{file_instance.file.name}"'
    
    return response


