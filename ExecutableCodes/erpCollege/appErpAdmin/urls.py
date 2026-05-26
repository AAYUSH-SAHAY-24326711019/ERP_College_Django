from django.urls import path
from . import views

urlpatterns = [

    # =========================
    # ADMIN LOGIN
    # =========================
    path(
        '',
        views.admin_login,
        name='admin_login'
    ),

    path(
        'logout/',
        views.admin_logout,
        name='admin_logout'
    ),

    # =========================
    # CSV DOWNLOAD
    # =========================
    path(
        'download-mainsite-csv/',
        views.download_mainsite_csv,
        name='download_mainsite_csv'
    ),

    # =========================
    # COURSE SESSION
    # =========================
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

    
    path('show-student-course/',views.showStudentCourse,name='showStudentCourse'),

    path('form1/',views.form1,name='form1'),
    path('form1_all/',views.form1_all,name='form1_all'),
    path('form1_edit/<int:id>',views.form1_edit,name='form1_edit'),

    path('form2/',views.form2,name='form2'),
    
]