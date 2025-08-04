from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

STATUS_CHOICES = [
    ('active', 'Active'),
    ('terminated', 'Terminated'),
    ('resigned', 'Resigned'),
]

class StaffRecord(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    user_account_created = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.email})"


DEVICE_STATUS_CHOICES = [
    ('available', 'Available'),
    ('borrowed', 'Borrowed'),
    ('maintenance', 'Maintenance'),
    ('lost', 'Lost'),
    ('damaged', 'Damaged'),
]

class Device(models.Model):
    name = models.CharField(max_length=100)  # e.g., "Laptop", "Printer"
    model_brand = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=DEVICE_STATUS_CHOICES, default='available')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.serial_number})"



class BorrowRecord(models.Model):
    staff = models.ForeignKey(StaffRecord, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.PROTECT)
    pr_number = models.CharField(max_length=255)
    date_issued = models.DateTimeField(auto_now_add=True)
    date_returned = models.DateTimeField(null=True, blank=True)
    remarks = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.staff.full_name} - {self.device.name}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)