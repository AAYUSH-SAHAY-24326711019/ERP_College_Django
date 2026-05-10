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

    # +==================
    path("student-enrollment/", views.student_enrollment_page, name="student_enrollment_page"),
    # AJAX
    path("ajax/get-sessions/", views.get_sessions_by_course, name="get_sessions_by_course"),
    path("ajax/enroll-students/", views.enroll_students_to_session, name="enroll_students_to_session"),
    # +==================


]