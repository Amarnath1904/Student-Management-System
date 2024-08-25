from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("admin_dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("student_dashboard/", views.student_dashboard, name="student_dashboard"),
    path("manage_students/", views.manage_students, name="manage_students"),
    path("manage_fee_plans/", views.manage_fee_plans, name="manage_fee_plans"),
    path("manage_fees/", views.manage_fees, name="manage_fees"),
    path("view_fee_status/", views.view_fee_status, name="view_fee_status"),
    path('student/<int:student_id>/', views.student_detail, name='student_detail'),
]
