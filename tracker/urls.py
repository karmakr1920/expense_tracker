from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path('<int:exp_id>/update-expense/', views.update_expense, name='update_expense'),
    path('<int:exp_id>/delete-expense/', views.delete_expense, name='delete_expense'),
    path('report/', views.report_view, name='report'),
    path('set-budget/', views.set_monthly_budget, name='set_monthly_budget'),

    # Auth-related
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
