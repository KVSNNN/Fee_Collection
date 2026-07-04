from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Academy(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    name = models.Model
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    gst_number = models.CharField(max_length=50, blank=True, null=True)
    logo = models.ImageField(upload_to='academy_logos/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        verbose_name_plural = "Academies"

class Trainer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    specialization = models.CharField(max_length=255, blank=True, null=True)
    academy = models.ForeignKey(Academy, on_delete=models.CASCADE, related_name='trainers')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=255)
    academy = models.ForeignKey(Academy, on_delete=models.CASCADE, related_name='courses')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Batch(models.Model):
    name = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='batches')
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='batches')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.course.name}"

    class Meta:
        verbose_name_plural = "Batches"

class Student(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    student_id = models.CharField(max_length=50, unique=True, blank=True)
    admission_no = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    dob = models.DateField()
    parent_name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=20)
    alt_mobile = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField()
    address = models.TextField()
    joining_date = models.DateField()
    academy = models.ForeignKey(Academy, on_delete=models.CASCADE, related_name='students')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='students')
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='students')
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='students')
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2)
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    last_due_date = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.student_id:
            last_student = Student.objects.all().order_by('id').last()
            if not last_student:
                self.student_id = 'STU00001'
            else:
                last_id = last_student.student_id
                if last_id and last_id.startswith('STU'):
                    try:
                        num = int(last_id[3:]) + 1
                        self.student_id = f'STU{num:05d}'
                    except ValueError:
                        self.student_id = f'STU{last_student.id + 1:05d}'
                else:
                    self.student_id = f'STU{last_student.id + 1:05d}'
        
        if not self.last_due_date:
            self.last_due_date = self.joining_date
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.student_id})"

class PaymentEntry(models.Model):
    PERIOD_CHOICES = [
        ('1 Month', '1 Month'),
        ('3 Months', '3 Months'),
        ('6 Months', '6 Months'),
        ('1 Year', '1 Year'),
    ]
    MODE_CHOICES = [
        ('Cash', 'Cash'),
        ('Card', 'Card'),
        ('UPI', 'UPI'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Online', 'Online'),
    ]
    STATUS_CHOICES = [
        ('Paid', 'Paid'),
        ('Partial Payment', 'Partial Payment'),
    ]
    receipt_no = models.CharField(max_length=50, unique=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    academy = models.ForeignKey(Academy, on_delete=models.CASCADE, related_name='payments')
    payment_date = models.DateField(default=timezone.now)
    payment_period = models.CharField(max_length=20, choices=PERIOD_CHOICES, default='3 Months')
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_mode = models.CharField(max_length=20, choices=MODE_CHOICES, default='Cash')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    next_due_date = models.DateField()
    remarks = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Paid')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.balance > 0:
            self.status = 'Partial Payment'
        else:
            self.status = 'Paid'

        if not self.receipt_no:
            prefix = "RCP"
            setting = SystemSetting.objects.filter(key='receipt_prefix').first()
            if setting:
                prefix = setting.value
            
            last_payment = PaymentEntry.objects.all().order_by('id').last()
            if not last_payment:
                self.receipt_no = f'{prefix}00001'
            else:
                last_no = last_payment.receipt_no
                if last_no and last_no.startswith(prefix):
                    try:
                        num = int(last_no[len(prefix):]) + 1
                        self.receipt_no = f'{prefix}{num:05d}'
                    except ValueError:
                        self.receipt_no = f'{prefix}{last_payment.id + 1:05d}'
                else:
                    self.receipt_no = f'{prefix}{last_payment.id + 1:05d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.receipt_no} - {self.student.name}"

    class Meta:
        verbose_name_plural = "Payment Entries"

class Notification(models.Model):
    TYPE_CHOICES = [
        ('Info', 'Info'),
        ('Warning', 'Warning'),
        ('Alert', 'Alert'),
        ('Success', 'Success'),
    ]
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='Info')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class SystemSetting(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.key

class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)
    model_name = models.CharField(max_length=100)
    object_id = models.IntegerField(blank=True, null=True)
    object_repr = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.timestamp} - {self.user} - {self.action}"
