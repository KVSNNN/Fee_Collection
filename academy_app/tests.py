import datetime
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth.models import User
from academy_app.models import Academy, Course, Trainer, Batch, Student, PaymentEntry, SystemSetting

class FeeManagementSystemTests(TestCase):

    def setUp(self):
        # Create Academy
        self.academy = Academy.objects.create(
            name="Tennis Academy",
            code="TA",
            address="123 Road",
            phone="123456",
            email="ta@example.com",
            status="Active"
        )
        # Create Trainer
        self.trainer = Trainer.objects.create(
            name="Coach John",
            email="john@example.com",
            phone="123456",
            academy=self.academy
        )
        # Create Course
        self.course = Course.objects.create(
            name="Tennis Beginner",
            academy=self.academy
        )
        # Create Batch
        self.batch = Batch.objects.create(
            name="Morning A",
            course=self.course,\
            trainer=self.trainer
        )
        
        # System settings
        SystemSetting.objects.create(key='receipt_prefix', value='RCP')
        SystemSetting.objects.create(key='financial_year', value='2026-2027')

    def test_student_auto_id_and_due_date_initialization(self):
        """Test that Student IDs are auto-sequenced and last_due_date defaults to joining_date."""
        s1 = Student.objects.create(
            admission_no="ADM01",
            name="Student One",
            gender="Male",
            dob=datetime.date(2010, 1, 1),
            parent_name="Parent One",
            mobile="123",
            email="s1@example.com",
            address="Address",
            joining_date=datetime.date(2026, 7, 10),
            academy=self.academy,
            course=self.course,
            batch=self.batch,
            trainer=self.trainer,
            monthly_fee=Decimal('3000.00'),
            status="Active"
        )
        self.assertEqual(s1.student_id, "STU00001")
        self.assertEqual(s1.last_due_date, datetime.date(2026, 7, 10))

        s2 = Student.objects.create(
            admission_no="ADM02",
            name="Student Two",
            gender="Female",
            dob=datetime.date(2011, 2, 2),
            parent_name="Parent Two",
            mobile="456",
            email="s2@example.com",
            address="Address",
            joining_date=datetime.date(2026, 7, 12),
            academy=self.academy,
            course=self.course,
            batch=self.batch,
            trainer=self.trainer,
            monthly_fee=Decimal('3000.00'),
            status="Active"
        )
        self.assertEqual(s2.student_id, "STU00002")

    def test_receipt_number_auto_generation(self):
        """Test that receipt numbers are auto-sequenced based on receipt prefix."""
        s = Student.objects.create(
            admission_no="ADM03",
            name="Student Three",
            gender="Male",
            dob=datetime.date(2010, 1, 1),
            parent_name="Parent",
            mobile="123",
            email="s3@example.com",
            address="Address",
            joining_date=datetime.date(2026, 7, 10),
            academy=self.academy,
            course=self.course,
            batch=self.batch,
            trainer=self.trainer,
            monthly_fee=Decimal('3000.00'),
            status="Active"
        )
        
        p1 = PaymentEntry.objects.create(
            student=s,
            academy=self.academy,
            payment_date=datetime.date(2026, 7, 10),
            payment_period="1 Month",
            amount_due=Decimal('3000.00'),
            amount_paid=Decimal('3000.00'),
            balance=Decimal('0.00'),
            payment_mode="Cash",
            next_due_date=datetime.date(2026, 8, 10)
        )
        self.assertEqual(p1.receipt_no, "RCP00001")

        p2 = PaymentEntry.objects.create(
            student=s,
            academy=self.academy,
            payment_date=datetime.date(2026, 8, 10),
            payment_period="3 Months",
            amount_due=Decimal('9000.00'),
            amount_paid=Decimal('9000.00'),
            balance=Decimal('0.00'),
            payment_mode="UPI",
            next_due_date=datetime.date(2026, 11, 10)
        )
        self.assertEqual(p2.receipt_no, "RCP00002")

    def test_partial_payment_flagging(self):
        """Test that a payment is flagged as Partial Payment if there's a remaining balance."""
        s = Student.objects.create(
            admission_no="ADM04",
            name="Student Four",
            gender="Female",
            dob=datetime.date(2010, 1, 1),
            parent_name="Parent",
            mobile="123",
            email="s4@example.com",
            address="Address",
            joining_date=datetime.date(2026, 7, 10),
            academy=self.academy,
            course=self.course,
            batch=self.batch,
            trainer=self.trainer,
            monthly_fee=Decimal('3000.00'),
            status="Active"
        )
        
        # Scenario 1: Paid in Full
        p1 = PaymentEntry.objects.create(
            student=s,
            academy=self.academy,
            payment_date=datetime.date(2026, 7, 10),
            payment_period="1 Month",
            amount_due=Decimal('3000.00'),
            amount_paid=Decimal('3000.00'),
            balance=Decimal('0.00'),
            payment_mode="Cash",
            next_due_date=datetime.date(2026, 8, 10)
        )
        self.assertEqual(p1.status, "Paid")

        # Scenario 2: Partial Payment
        p2 = PaymentEntry.objects.create(
            student=s,
            academy=self.academy,
            payment_date=datetime.date(2026, 8, 10),
            payment_period="1 Month",
            amount_due=Decimal('3000.00'),
            amount_paid=Decimal('2000.00'),
            balance=Decimal('1000.00'),
            payment_mode="Cash",
            next_due_date=datetime.date(2026, 9, 10)
        )
        self.assertEqual(p2.status, "Partial Payment")
