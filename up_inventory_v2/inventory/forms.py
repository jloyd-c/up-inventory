import os
from django import forms
from .models import StaffRecord, Department, Device, BorrowRecord, Location

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
        fields = ['name', 'model_brand', 'serial_number', 'location', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'model_brand': forms.TextInput(attrs={'class': 'form-control'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_serial_number(self):
        serial_number = self.cleaned_data['serial_number']
        if self.instance.pk:  # If editing existing device
            if Device.objects.filter(serial_number=serial_number).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("This serial number already exists.")
        else:  # If creating new device
            if Device.objects.filter(serial_number=serial_number).exists():
                raise forms.ValidationError("This serial number already exists.")
        return serial_number

    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            if image.size > 2*1024*1024:  # 2MB limit
                raise forms.ValidationError("Image file too large ( > 2MB )")
            return image
        return None








class ReturnForm(forms.Form):
    borrow_record = forms.ModelChoiceField(
        queryset=BorrowRecord.objects.filter(date_returned__isnull=True),
        label="Select Borrowed Record"
    )
    return_remarks = forms.CharField(required=False, widget=forms.Textarea)
    device_status = forms.ChoiceField(choices=[
        ('available', 'Available'),
        ('damaged', 'Damaged'),
        ('maintenance', 'Maintenance'),
        ('lost', 'Lost'),
        ('condemned', 'Condemned'),
    ])

class BorrowForm(forms.ModelForm):
    class Meta:
        model = BorrowRecord
        fields = ['staff', 'device', 'pr_number', 'remarks']

    def __init__(self, *args, **kwargs):
        available_devices = kwargs.pop('available_devices', None)
        active_staff = kwargs.pop('active_staff', None)
        super().__init__(*args, **kwargs)

        if active_staff is not None:
            self.fields['staff'].queryset = active_staff
        if available_devices is not None:
            self.fields['device'].queryset = available_devices








class ReturnEditForm(forms.ModelForm):
    device_status = forms.ChoiceField(choices=[
        ('available', 'Available'),
        ('damaged', 'Damaged'),
        ('maintenance', 'Maintenance'),
        ('lost', 'Lost'),
        ('condemned', 'Condemned'),
    ])

    class Meta:
        model = BorrowRecord
        fields = ['remarks', 'device_status']
        widgets = {
            'remarks': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        # Set initial device_status from the related device's status
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['device_status'].initial = self.instance.device.status

    def save(self, commit=True):
        borrow_record = super().save(commit=False)
        device_status = self.cleaned_data['device_status']
        # Update device status as well
        device = borrow_record.device
        device.status = device_status
        device.save()
        if commit:
            borrow_record.save()
        return borrow_record




class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Location Name'})
        }