import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'academy_project.settings')
django.setup()

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from academy_app.models import Academy, Course, Trainer, Batch, Student, SystemSetting
import datetime

def setup_all():
    print("Initializing Database...")
    
    # 1. Create Superuser
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("Superuser 'admin' created (password: admin123).")
    else:
        print("Superuser 'admin' already exists.")

    # 2. Create Roles / Groups
    roles = ['Administrator', 'Manager', 'Reception', 'Accountant', 'Read Only User']
    for role in roles:
        group, created = Group.objects.get_or_create(name=role)
        if created:
            print(f"Group '{role}' created.")
    
    # 3. Create Default System Settings
    settings_dict = {
        'receipt_prefix': 'RCP',
        'financial_year': '2026-2027',
        'sms_enabled': 'False',
        'email_enabled': 'False',
        'whatsapp_enabled': 'False',
    }
    for key, value in settings_dict.items():
        setting, created = SystemSetting.objects.get_or_create(key=key, defaults={'value': value})
        if created:
            print(f"Setting '{key}' set to '{value}'.")

    # 4. Create Mock Data for Academies, Courses, Trainers, Batches, Students
    if Academy.objects.count() == 0:
        a1 = Academy.objects.create(
            name="Champions Tennis Academy",
            code="CTA",
            address="123 Sports Drive, Sector 4",
            phone="9876543210",
            email="info@champions.com",
            gst_number="29AAAAA1111A1Z1",
            status="Active"
        )
        a2 = Academy.objects.create(
            name="Elite Cricket Academy",
            code="ECA",
            address="456 Stadium Road, Block B",
            phone="9876543211",
            email="contact@elitecricket.com",
            gst_number="29BBBBB2222B1Z2",
            status="Active"
        )
        print("Mock academies created.")

        t1 = Trainer.objects.create(
            name="Coach Hari Prasad",
            email="hari@champions.com",
            phone="9811122233",
            specialization="Advanced Clay Court Tennis",
            academy=a1
        )
        t2 = Trainer.objects.create(
            name="Coach Harish Kumar",
            email="harish@elitecricket.com",
            phone="9811122244",
            specialization="Fast Bowling",
            academy=a2
        )
        print("Mock trainers created.")

        c1 = Course.objects.create(
            name="Tennis Pro Program",
            academy=a1,
            description="Intensive tennis course"
        )
        c2 = Course.objects.create(
            name="Cricket Masters Program",
            academy=a2,
            description="Cricket technique course"
        )
        print("Mock courses created.")

        b1 = Batch.objects.create(
            name="Morning Batch A",
            course=c1,
            trainer=t1
        )
        b2 = Batch.objects.create(
            name="Evening Batch B",
            course=c2,
            trainer=t2
        )
        print("Mock batches created.")

        # Let's add some mock students to demonstrate smart search
        Student.objects.create(
            admission_no="ADM0001",
            name="Harikrishnan S",
            gender="Male",
            dob=datetime.date(2010, 5, 12),
            parent_name="Sundar",
            mobile="9888877777",
            email="hari@gmail.com",
            address="Indiranagar, Bangalore",
            joining_date=datetime.date(2026, 1, 10),
            academy=a1,
            course=c1,
            batch=b1,
            trainer=t1,
            monthly_fee=3000.00,
            registration_fee=500.00,
            discount=0.00,
            status="Active",
            last_due_date=datetime.date(2026, 7, 10)
        )
        Student.objects.create(
            admission_no="ADM0002",
            name="Haroon Rasheed",
            gender="Male",
            dob=datetime.date(2012, 8, 25),
            parent_name="Rasheed",
            mobile="9777766666",
            email="haroon@gmail.com",
            address="Whitefield, Bangalore",
            joining_date=datetime.date(2026, 2, 15),
            academy=a1,
            course=c1,
            batch=b1,
            trainer=t1,
            monthly_fee=3000.00,
            registration_fee=500.00,
            discount=200.00,
            status="Active",
            last_due_date=datetime.date(2026, 7, 15)
        )
        Student.objects.create(
            admission_no="ADM0003",
            name="Harish Sen",
            gender="Male",
            dob=datetime.date(2011, 2, 20),
            parent_name="Sen",
            mobile="9666655555",
            email="harish.sen@gmail.com",
            address="Koramangala, Bangalore",
            joining_date=datetime.date(2026, 3, 1),
            academy=a2,
            course=c2,
            batch=b2,
            trainer=t2,
            monthly_fee=3500.00,
            registration_fee=1000.00,
            discount=500.00,
            status="Active",
            last_due_date=datetime.date(2026, 7, 1)
        )
        print("Mock students created for autocomplete testing.")

if __name__ == '__main__':
    setup_all()
