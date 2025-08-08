from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Location(models.Model):
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
    ('issued', 'Issued'),
    ('maintenance', 'Maintenance'),
    ('lost', 'Lost'),
    ('damaged', 'Damaged'),
    ('condemned', 'Condemned'),
]

class Device(models.Model):
    name = models.CharField(max_length=100)  # e.g., "Laptop", "Printer"
    model_brand = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=DEVICE_STATUS_CHOICES, default='available')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='device_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.serial_number})"
    
    def get_status_display(self):
        """Get human-readable status"""
        return dict(DEVICE_STATUS_CHOICES).get(self.status, self.status)

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

class HistoryLog(models.Model):
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('borrow', 'Borrow'),
        ('return', 'Return'),
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('user_create', 'User Create'),
        ('user_update', 'User Update'),
        ('user_delete', 'User Delete'),
    ]

    user = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=50)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    details = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'History Log'
        verbose_name_plural = 'History Logs'

    def __str__(self):
        return f"{self.get_action_display()} {self.model_name} by {self.user} at {self.timestamp}"