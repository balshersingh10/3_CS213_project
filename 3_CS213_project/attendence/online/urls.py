from django.urls import path
from . import views


urlpatterns = [
    path("",views.index, name="index"),
    path("login_view" , views.login_view , name="login_view"),
    path("logout_view" , views.logout_view , name="logout_view"),
    path("<int:course_id>" , views.course_detail , name="course_detail"),
    path("mark_attendence/<int:course_idd>", views.mark_attendence, name="mark_attendence"),
    path("view_attendence/<slug:code>", views.view_attendence, name="view_attendence"),
    path("register", views.register , name ="register"),
    path("register_course", views.register_course, name="register_course"),
    path("join_coursee/<slug:code>", views.join_course, name="join_course"),
    path("enroll", views.enroll, name="enroll"),
    path("find", views.find, name="find"),
    path("enroll_course", views.enroll_course, name="enroll_course"),
    path("view_fac/<int:course_id>", views.view_fac, name="view_fac"),
    path("stats", views.stats, name="stats"),
    path("find_stat_roll", views.find_stat_roll, name="find_stat_roll"),
    path("find_stat_code", views.find_stat_code, name="find_stat_code"),
    path("defaulter/<slug:code>", views.defaulter, name="defaulter")
]
