from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'CGS_Dashboard'
urlpatterns = [
  path('dashboard/', views.dashboard, name='dashboard'),

  
  path('doctoral_courses_dashboard/', views.doctoral_courses_dashboard, name='doctoral_courses_dashboard'),
  path('doctoral_students/<str:programs>/', views.doctoral_student_list_view, name='doctoral_student_list'),
  
  #masteral dashboard
  path('masteral_courses_dashboard/', views.masteral_courses_dashboard, name='masteral_courses_dashboard'),
  path('masteral/<str:majors>/', views.masteral_student_list_view, name='masteral_student_list'),
  path('master_of_management/', views.master_of_management_list_view, name='master_of_management_list'),
 
] 

# Serve media files during development
if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static files during development (optional; Django does this automatically when DEBUG=True)
if settings.DEBUG:
  urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



