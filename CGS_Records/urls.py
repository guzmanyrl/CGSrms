from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'CGS_Records'
urlpatterns = [
  
 
 path ('base/', views.base, name = 'base'),
 
  #Doctoral Url Patterns
  path('doctoral/', views.doctoral, name='doctoral'),
  path('docrol_evalaution/', views.doctoral_evaluation, name='doctoral_evaluation'),
  path('doctoral_list/', views.doctoral_list, name='doctoral_list'),
  path('add_doctoral_student/', views.add_doctoral_student, name='add_doctoral_student'),
  path('doctoral/edit/<str:student_id>/', views.edit_doctoral_student, name='edit_doctoral_student'),
  path('doctoral/remove/<str:student_id>/', views.remove_doctoral_student, name='remove_doctoral_student'),
  path('view-file/<str:model_name>/<int:file_id>/', views.view_file_inline, name='view_file_inline'),
  path('student/<str:student_id>/files/manage/', views.manage_student_files, name='manage_student_files'),
  path('student/<str:student_id>/files/upload/', views.upload_files, name='upload_files'),
  path('docotral_update_profile_picture/<str:student_id>/', views.doctoral_update_profile_picture, name='docotral_update_profile_picture'),

  #Masteral Url Patterns
  path('masteral/',views.masteral, name = 'masteral'),
  path('masteral_list/', views.masteral_list, name='masteral_list'),
  path('add_masteral_student/', views.add_masteral_student, name='add_masteral_student'),
  path('masteral/edit/<str:student_id>/', views.edit_masteral_student, name='edit_masteral_student'),
  path('masteral/remove/<str:student_id>/', views.remove_masteral_student, name='remove_masteral_student'),
  path('view-masteral-file/<str:model_name>/<int:file_id>/', views.view_masteral_file_inline, name='view_masteral_file_inline'),
  path('student/<str:student_id>/files/manage-masteral/', views.manage_masteral_student_files, name='manage_masteral_student_files'),
  path('student/<str:student_id>/files/upload-masteral/', views.upload_masteral_files, name='upload_masteral_files'),
  path('masteral_update_profile_picture/<str:student_id>/', views.masteral_update_profile_picture, name='masteral_update_profile_picture'),
  
  #Faculty Url Patterns
  path('faculty/',views.faculty,name='faculty'),
  path('faculty-list', views.faculty_list, name='faculty_list'),
  path('faculty/add/', views.add_faculty, name='add_faculty'),
  path('faculty/edit/<str:faculty_id>/', views.edit_faculty, name='edit_faculty'),
  path('faculty/remove/<str:faculty_id>/', views.remove_faculty, name='remove_faculty'),
  path('faculty/<str:faculty_id>/faculty-files/', views.manage_faculty_files, name='manage_faculty_files'),
  path('faculty/<str:faculty_id>/faculty-upload/', views.upload_faculty_files, name='upload_faculty_files'),
  path('faculty/<int:file_id>/faculty-view-file/<str:model_name>/', views.view_faculty_file_inline, name='view_faculty_file_inline'),
  path('faculty_update_profile_picture/<str:faculty_id>/', views.faculty_update_profile_picture, name='faculty_update_profile_picture'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

