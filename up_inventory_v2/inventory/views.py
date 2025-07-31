from django.shortcuts import render, redirect, get_object_or_404
from .models import StaffRecord, Department, Device
from .forms import StaffRecordForm, DepartmentForm, DeviceForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q

# Create your views here.
def home_view(request):
    return render(request, 'home.html')

def test_view(request):
    return render(request, 'test_modal.html')

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')

@login_required
def inventory_view(request):
    return render(request, 'inventory.html')







@login_required
def staff_list(request):
    query = request.GET.get("q", "")

    if query:
        staff_records = StaffRecord.objects.filter(
            Q(full_name__icontains=query) |
            Q(email__icontains=query) |
            Q(status__icontains=query) |
            Q(department__name__icontains=query)
        ).order_by('-created_at')
    else:
        staff_records = StaffRecord.objects.all().order_by('-created_at')

    form = StaffRecordForm()
    departments = Department.objects.all()

    if request.method == 'POST' and request.POST.get("id"):
        staff = get_object_or_404(StaffRecord, pk=request.POST["id"])
        form = StaffRecordForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            return redirect('staff')

    return render(request, 'staff.html', {
        'staff_records': staff_records,
        'form': form,
        'departments': departments,
        'query': query
    })



@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_staff(request):
    if request.method == 'POST':
        form = StaffRecordForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('staff')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def update_staff(request, pk):
    staff = get_object_or_404(StaffRecord, pk=pk)
    if request.method == 'POST':
        form = StaffRecordForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
    return redirect('staff')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_staff(request, pk):
    staff = get_object_or_404(StaffRecord, pk=pk)
    staff.delete()
    return redirect('staff')


import openpyxl
from django.http import HttpResponse
from django.utils.encoding import smart_str

@login_required
def export_staff_excel(request):
    query = request.GET.get("q", "")
    staff_records = StaffRecord.objects.filter(full_name__icontains=query) if query else StaffRecord.objects.all().order_by('-created_at')

    # Create an Excel workbook and sheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Staff Records"

    # Header row
    ws.append(["Full Name", "Email", "Status", "Department", "date"])

    # Data rows
    for staff in staff_records:
        ws.append([
            staff.full_name,
            staff.email,
            staff.status,
            staff.department.name if staff.department else '',
            staff.created_at.strftime("%Y-%m-%d %H:%M:%S") if staff.created_at else '',
        ])

    # Prepare response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=staff_records.xlsx'

    wb.save(response)
    return response















@login_required
def department_list(request):
    query = request.GET.get("q", "")
    if query:
        departments = Department.objects.filter(name__icontains=query).order_by('-created_at')
    else:
        departments = Department.objects.all().order_by('-created_at')

    form = DepartmentForm()

    # Handle edit form submission
    if request.method == 'POST' and request.POST.get("id"):
        dept = get_object_or_404(Department, pk=request.POST["id"])
        form = DepartmentForm(request.POST, instance=dept)
        if form.is_valid():
            form.save()
            return redirect('department')

    return render(request, 'department.html', {
        'departments': departments,
        'form': form,
        'query': query
    })

@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('department')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_department(request, pk):
    dept = get_object_or_404(Department, pk=pk)
    dept.delete()
    return redirect('department')

import openpyxl
from django.http import HttpResponse

@login_required
def export_department_excel(request):
    query = request.GET.get("q", "")
    departments = Department.objects.filter(name__icontains=query) if query else Department.objects.all().order_by('-created_at')

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Departments"

    ws.append(["Department Name", "Date Created"])

    for dept in departments:
        ws.append([
            dept.name,
            dept.created_at.strftime("%Y-%m-%d %H:%M:%S") if dept.created_at else ''
        ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=departments.xlsx'

    wb.save(response)
    return response
















@login_required
def device_list(request):
    query = request.GET.get("q", "")

    if query:
        devices = Device.objects.filter(
            Q(name__icontains=query) |
            Q(model_brand__icontains=query) |
            Q(serial_number__icontains=query) |
            Q(status__icontains=query)
        )
    else:
        devices = Device.objects.all()

    form = DeviceForm()

    if request.method == 'POST' and request.POST.get("id"):
        device = get_object_or_404(Device, pk=request.POST["id"])
        form = DeviceForm(request.POST, instance=device)
        if form.is_valid():
            form.save()
            return redirect('devices')

    return render(request, 'devices.html', {
        'devices': devices,
        'form': form,
        'query': query
    })

@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_device(request):
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('devices')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def update_device(request, pk):
    device = get_object_or_404(Device, pk=pk)
    if request.method == 'POST':
        form = DeviceForm(request.POST, instance=device)
        if form.is_valid():
            form.save()
    return redirect('devices')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_device(request, pk):
    device = get_object_or_404(Device, pk=pk)
    device.delete()
    return redirect('devices')

import openpyxl
from django.http import HttpResponse

@login_required
def export_device_excel(request):
    query = request.GET.get("q", "")
    devices = Device.objects.filter(name__icontains=query) if query else Device.objects.all()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Devices"

    ws.append(["Name", "Model/Brand", "Serial Number", "Status"])

    for device in devices:
        ws.append([
            device.name,
            device.model_brand,
            device.serial_number,
            device.status,
        ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=devices.xlsx'

    wb.save(response)
    return response
