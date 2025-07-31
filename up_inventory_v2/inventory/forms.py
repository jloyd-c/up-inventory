from django import forms
from .models import StaffRecord, Department, Device

class StaffRecordForm(forms.ModelForm):
    class Meta:
        model = StaffRecord
        fields = ['full_name', 'email', 'status', 'department']

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Department Name'})
        }

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['name', 'model_brand', 'serial_number', 'status']