from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from CGS_Records.models import DoctoralStudents,MasteralStudents,Faculty
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_list_or_404
from django.template.loader import render_to_string
from django.conf import settings
import os
from django.urls import reverse
from django.db.models import Q
import pdfkit
config = pdfkit.configuration(wkhtmltopdf=settings.WKHTMLTOPDF_PATH)


# Create your views here.


#Doctoral Dashboard
@login_required(login_url='accounts:home_login')
def dashboard(request):
    # Count only entries with non-empty student_id for students (Total counts)
    doctoral_total = DoctoralStudents.objects.filter(~Q(student_id="")).count()
    masteral_total = MasteralStudents.objects.filter(~Q(student_id="")).count()
    
    # Count only entries with non-empty faculty_id for faculty (Total count)
    total_faculty = Faculty.objects.filter(~Q(faculty_id="")).count()

    # Print to check values in the console (for debugging)
    print("Doctoral Total:", doctoral_total)
    print("Masteral Total:", masteral_total)
    print("Total Faculty:", total_faculty)

    # Start with all students (unfiltered)
    students = DoctoralStudents.objects.all()

    # Apply filters if present
    school_year = request.GET.get('school_year', '')
    programs = request.GET.get('program', '')
    semester = request.GET.get('semester', '')
    student_type = request.GET.get('student_type', '')

    if school_year:
        students = students.filter(school_year=school_year)
    if programs:
        students = students.filter(programs=programs)
    if semester:
        students = students.filter(semester=semester)
    if student_type:
        students = students.filter(student_type=student_type)

    # Retrieve counts for each major (this part will respect the filters)
    programs_counts = {
        programs[0]: students.filter(programs=programs[0]).count()
        for programs in DoctoralStudents.PROGRAMS_CHOICES
    }

    context = {
        'programs_counts': programs_counts,
        'school_year_choices': DoctoralStudents.SCHOOL_YEAR_CHOICES,
        'doctoral_program_choices': DoctoralStudents.PROGRAMS_CHOICES,
        'semester_choices': DoctoralStudents.SEMESTER_CHOICES,
        'student_type_choices': DoctoralStudents.STUDENT_TYPE_CHOICES,
        # Add the statistics overview data to the context (totals remain unaffected by filters)
        'doctoral_total': doctoral_total,  # Total students, not affected by filters
        'masteral_total': masteral_total,  # Total students, not affected by filters
        'total_faculty': total_faculty,    # Total faculty, not affected by filters
    }

    return render(request, 'Dashboard/dashboard.html', context)

@login_required(login_url='accounts:home_login')
def doctoral_courses_dashboard(request):
    # Fetch filter criteria from request
    selected_school_year = request.GET.get('school_year')
    selected_program = request.GET.get('programs')
    selected_semester = request.GET.get('semester')
    selected_student_type = request.GET.get('student_type')

    # Filter students based on selected criteria
    students = DoctoralStudents.objects.all()
    if selected_school_year:
        students = students.filter(school_year=selected_school_year)
    if selected_program:
        students = students.filter(programs=selected_program)
    if selected_semester:
        students = students.filter(semesters=selected_semester)
    if selected_student_type:
        students = students.filter(student_type=selected_student_type)

    # Count students by major dynamically based on filtered students
    programs_counts = {
        programs[0]: students.filter(programs=programs[0]).count()
        for programs in DoctoralStudents.PROGRAMS_CHOICES
    }

    context = {
        'doctoral_majors_counts': programs_counts,
        'school_year_choices': DoctoralStudents.SCHOOL_YEAR_CHOICES,
        'doctoral_program_choices': DoctoralStudents.PROGRAMS_CHOICES,
        'semester_choices': DoctoralStudents.SEMESTER_CHOICES,
        'student_type_choices': DoctoralStudents.STUDENT_TYPE_CHOICES,
    }
    return render(request, 'Dashboard/dashboard.html', context)

@login_required(login_url='accounts:home_login')
def doctoral_student_list_view(request, programs):
    students = DoctoralStudents.objects.filter(programs=programs)

    # Apply filters from GET parameters
    school_year = request.GET.get('school_year')
    programs = request.GET.get('programs')
    semester = request.GET.get('semester')
    student_type = request.GET.get('student_type')

    if school_year:
        students = students.filter(school_year=school_year)
    if programs:
        students = students.filter(programs=programs)
    if semester:
        students = students.filter(semesters=semester)
    if student_type:
        students = students.filter(student_type=student_type)
        
    students = students.order_by('last_name')

    context = {
        'students': students,
        'programs': programs,
        'is_pdf': False,
    }

    # PDF generation remains the same
    if request.GET.get('download') == 'pdf':
        context['is_pdf'] = True
        html = render_to_string('Dashboard/doctoral_generate_list.html', context, request=request)

        options = {
            'page-size': 'Letter',  # Short bond paper size
            'margin-top': '0.5in',
            'margin-right': '0.5in',
            'margin-bottom': '0.5in',
            'margin-left': '0.5in',
            'enable-local-file-access': '',
            'no-stop-slow-scripts': '',
            'disable-smart-shrinking': '',
            'javascript-delay': 2000,  # Allow time for dynamic rendering
        }

        pdf = pdfkit.from_string(html, False, configuration=config, options=options)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{programs}_students.pdf"'
        return response

    return render(request, 'Dashboard/doctoral_generate_list.html', context)

# Masteral Dashboard
@login_required(login_url='accounts:home_login')
def masteral_dashboard(request):
    mstudents = MasteralStudents.objects.all()
    majors_counts = {
        majors[0]: mstudents.filter(majors=majors[0]).count()
        for majors in MasteralStudents.MAJORS_CHOICES
    }
    
    # Add URL for Master of Management students list
    master_of_management_url = reverse('CGS_Dashboard:master_of_management_list')  # Make sure this name matches your URL name
    
    context = {
        'majors_counts': majors_counts,
        'school_year_choices': MasteralStudents.SCHOOL_YEAR_CHOICES,
        'masteral_program_choices': MasteralStudents.PROGRAMS_CHOICES,
        'semester_choices': MasteralStudents.SEMESTER_CHOICES,
        'student_type_choices': MasteralStudents.STUDENT_TYPE_CHOICES,
        'master_of_management_url': master_of_management_url,  # Add this to context
    }
    return render(request, 'Dashboard/dashboard.html', context)


@login_required(login_url='accounts:home_login')
def masteral_courses_dashboard(request):
    selected_school_year = request.GET.get('school_year')
    selected_program = request.GET.get('program')
    selected_semester = request.GET.get('semester')
    selected_student_type = request.GET.get('student_type')

    # Filter students based on selected criteria
    mstudents = MasteralStudents.objects.all()
    if selected_school_year:
        mstudents = mstudents.filter(school_year=selected_school_year)
    if selected_program:
        mstudents = mstudents.filter(programs=selected_program)
    if selected_semester:
        mstudents = mstudents.filter(semesters=selected_semester)
    if selected_student_type:
        mstudents = mstudents.filter(student_type=selected_student_type)

    # Count majors dynamically
    majors_counts = {
        majors[0]: mstudents.filter(majors=majors[0]).count()
        for majors in MasteralStudents.MAJORS_CHOICES
    }

    # Count for Master of Management Program
    master_of_management_count = mstudents.filter(programs='Master of Management').count()

    context = {
        'masteral_majors_counts': majors_counts,
        'master_of_management_count': master_of_management_count,
        'school_year_choices': MasteralStudents.SCHOOL_YEAR_CHOICES,
        'masteral_program_choices': MasteralStudents.PROGRAMS_CHOICES,
        'semester_choices': MasteralStudents.SEMESTER_CHOICES,
        'student_type_choices': MasteralStudents.STUDENT_TYPE_CHOICES,
    }
    return render(request, 'Dashboard/dashboard.html', context)



@login_required(login_url='accounts:home_login')
def masteral_student_list_view(request, majors):
    # Filter students by major
    mstudents = MasteralStudents.objects.filter(majors=majors)

    # Apply filters from GET parameters
    school_year = request.GET.get('school_year')
    selected_program = request.GET.get('program')
    semester = request.GET.get('semester')
    student_type = request.GET.get('student_type')

    if school_year:
        mstudents = mstudents.filter(school_year=school_year)
    if selected_program:
        mstudents = mstudents.filter(programs=selected_program)
    if semester:
        mstudents = mstudents.filter(semesters=semester)
    if student_type:
        mstudents = mstudents.filter(student_type=student_type)

    # Order students alphabetically by last_name
    mstudents = mstudents.order_by('last_name')

    context = {
        'mstudents': mstudents,
        'majors': majors,
        'is_pdf': False,
    }

    # PDF generation remains the same
    if request.GET.get('download') == 'pdf':
        context['is_pdf'] = True
        html = render_to_string('Dashboard/masteral_generate_list.html', context)

        options = {
            'page-size': 'Legal',
            'margin-top': '0.5in',
            'margin-right': '0.5in',
            'margin-bottom': '0.5in',
            'margin-left': '0.5in',
            'no-stop-slow-scripts': '',
            'disable-smart-shrinking': '',
            'enable-local-file-access': '',
            'javascript-delay': 2000,
        }

        pdf = pdfkit.from_string(html, False, configuration=config, options=options)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{majors}_mstudents.pdf"'
        return response

    return render(request, 'Dashboard/masteral_generate_list.html', context)


@login_required(login_url='accounts:home_login')
def master_of_management_list_view(request):
    mstudents = MasteralStudents.objects.filter(programs='Master of Management')
    
    # PDF handling logic
    is_pdf = request.GET.get('download') == 'pdf'
    context = {
        'mstudents': mstudents,
        'programs': 'Master of Management',
        'is_pdf': is_pdf,
    }
    
    if is_pdf:
        html = render_to_string('Dashboard/master_of_management_list.html', context)
        options = {
            'page-size': 'Legal',
            'margin-top': '0.5in',
            'margin-right': '0.5in',
            'margin-bottom': '0.5in',
            'margin-left': '0.5in',
            'no-stop-slow-scripts': '',
            'disable-smart-shrinking': '',
            'enable-local-file-access': '',
            'javascript-delay': 2000,
        }
        pdf = pdfkit.from_string(html, False, options=options)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="master_of_management_students.pdf"'
        return response
    
    return render(request, 'Dashboard/master_of_management_list.html', context)


def statistics_overview(request):
    # Count only entries with non-empty student_id for students
    doctoral_total = DoctoralStudents.objects.filter(~Q(student_id="")).count()
    masteral_total = MasteralStudents.objects.filter(~Q(student_id="")).count()
    
    # Count only entries with non-empty faculty_id for faculty
    total_faculty = Faculty.objects.filter(~Q(faculty_id="")).count()

    # Print to check values in the console
    print("Doctoral Total:", doctoral_total)
    print("Masteral Total:", masteral_total)
    print("Total Faculty:", total_faculty)

    context = {
        'doctoral_total': doctoral_total,
        'masteral_total': masteral_total,
        'total_faculty': total_faculty,
    }

    return render(request, 'Dashboard/dashboard.html', context)
