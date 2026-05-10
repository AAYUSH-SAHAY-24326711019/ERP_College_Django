from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_login, name='admin_login'),
    path('download-mainsite-csv/',views.download_mainsite_csv,name='download_mainsite_csv'),
    path('logout/',views.admin_logout,name='admin_logout'),
    path(
        'course-session-page/',
        views.course_session_page,
        name='course_session_page'
    ),

    path(
        'save-course-session/',
        views.save_course_session,
        name='save_course_session'
    ),

 path(
        'add-students-to-course/',
        views.add_students_to_course,
        name='add_students_to_course'
    ),



    path(
        'get-students-preview/',
        views.get_students_preview,
        name='get_students_preview'
    ),

]