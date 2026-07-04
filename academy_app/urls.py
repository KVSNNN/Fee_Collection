from django.urls import path
from academy_app import views

urlpatterns = [
    # Auth
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Core Dashboard & Management
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('academies/', views.academies_view, name='academies'),
    path('students/', views.students_view, name='students'),
    path('students/import/excel/', views.import_students_view, name='import_students'),
    
    # Payment Desk & Receipts
    path('payment-desk/', views.payment_desk_view, name='payment_desk'),
    path('payment/create/', views.payment_create_view, name='payment_create'),
    path('receipt/<int:pk>/pdf/', views.receipt_pdf_view, name='receipt_pdf'),
    
    # Reports & Exports
    path('reports/', views.reports_view, name='reports'),
    path('reports/export/csv/', views.export_csv_view, name='export_csv'),
    path('reports/export/excel/', views.export_excel_view, name='export_excel'),
    
    # Settings & Configurations
    path('settings/', views.settings_view, name='settings'),
    path('settings/update/', views.update_settings_view, name='update_settings'),
    path('settings/create-course/', views.create_course_view, name='create_course'),
    path('settings/create-batch/', views.create_batch_view, name='create_batch'),
    path('settings/create-trainer/', views.create_trainer_view, name='create_trainer'),
    
    # System Alerts
    path('notifications/mark-read/', views.mark_notifications_read_view, name='mark_notifications_read'),
    
    # Backup utilities
    path('backup/trigger/', views.trigger_backup_view, name='trigger_backup'),
    path('backup/restore/', views.restore_backup_view, name='restore_backup'),
    
    # Autocomplete APIs
    path('api/students/search/', views.api_student_search, name='api_student_search'),
    path('api/students/<int:pk>/details/', views.api_student_details, name='api_student_details'),
    path('api/settings/metadata/', views.api_settings_metadata, name='api_settings_metadata'),
]
