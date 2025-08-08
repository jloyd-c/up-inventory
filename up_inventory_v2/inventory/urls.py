from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('dashboard', views.dashboard_view, name='dashboard'),
    path('inventory', views.inventory_view, name='inventory'),
    path('test', views.test_view, name='test'),


    path('staff/', views.staff_list, name='staff'),
    path('staff/add/', views.add_staff, name='add_staff'),
    path('staff/update/<int:pk>/', views.update_staff, name='update_staff'),
    path('staff/delete/<int:pk>/', views.delete_staff, name='delete_staff'),
    path('export_staff_excel/', views.export_staff_excel, name='export_staff_excel'),




    path('departments/', views.department_list, name='department'),
    path('departments/add/', views.add_department, name='add_department'),
    path('departments/delete/<int:pk>/', views.delete_department, name='delete_department'),
    path('departments/export/', views.export_department_excel, name='export_department_excel'),
    path('update/<int:pk>/', views.department_list, name='update_department'),




    path('devices/', views.device_list, name='devices'),
    path('devices/add/', views.add_device, name='add_device'),
    path('devices/update/<int:pk>/', views.update_device, name='update_device'),
    path('devices/delete/<int:pk>/', views.delete_device, name='delete_device'),
    path('devices/export/', views.export_device_excel, name='export_device_excel'),




    path('borrow-return/', views.inventory_view, name='borrow_return'),
    path('inventory/export_excel/', views.export_inventory_excel, name='export_inventory_excel'),
    path('return/edit/<int:pk>/', views.return_edit_view, name='return_edit'),
    path('return/delete/<int:pk>/', views.return_delete_view, name='return_delete'),
    path('download-inventory-pdf/', views.download_inventory_pdf, name='download_inventory_pdf'),




    path('locations/', views.location_list, name='location'),
    path('locations/add/', views.add_location, name='add_location'),
    path('locations/delete/<int:pk>/', views.delete_location, name='delete_location'),
    path('locations/export/', views.export_location_excel, name='export_location_excel'),


    

    path('history/', views.history_log, name='history_log'),
    path('history/delete/<int:log_id>/', views.delete_history_log, name='delete_history_log'),
    path('history/clear/', views.clear_history_logs, name='clear_history_logs'),
    path('history/export/', views.export_history_excel, name='export_history_excel'),

    # In your urls.py
    path('devices/<int:pk>/view/', views.view_device, name='view_device'),
]