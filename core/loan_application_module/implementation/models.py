from django.db import models
from django.utils import timezone

from django.conf import settings

from decimal import Decimal


class Client(models.Model):
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    middle_name = models.CharField(max_length=100, blank=True)
    national_id = models.CharField(max_length=50, unique=True)
    gender = models.CharField(max_length=10, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    marital_status = models.CharField(max_length=20, blank=True)
    phone_number = models.CharField(max_length=100, blank=True)
    alternate_phone_number = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    county = models.CharField(max_length=100, blank=True)
    sub_county = models.CharField(max_length=100, blank=True)
    ward = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    physical_address = models.TextField(blank=True)
    employment_status = models.CharField(max_length=50, blank=True)
    employer_name = models.CharField(max_length=255, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    work_location = models.CharField(max_length=255, blank=True, null=True)
    other_income_source = models.CharField(max_length=100, blank=True)
    monthly_income = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    other_income_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    consent_credit_check = models.BooleanField(default=False)
    consent_data_processing = models.BooleanField(default=False)

    # business
    business_name = models.CharField(max_length=255, blank=True)
    business_type = models.CharField(max_length=100, blank=True)
    business_location = models.CharField(max_length=255, blank=True)
    business_income = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    business_age = models.CharField( max_length=50, null=True, blank=True)

    # financial
    bank_name = models.CharField(max_length=400, blank=True)
    account_number = models.CharField(max_length=50, blank=True)
    mpesaNumber = models.CharField(max_length=50, blank=True)

    # terms and conditions
    accepted_terms = models.BooleanField(default=False)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="clients_created",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} ({self.national_id})"


class NextOfKin(models.Model):
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="next_of_kin"
    )
    name = models.CharField(max_length=255)
    relationship = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name
    

class LoanApplication(models.Model):
    STATUS_PENDING = "PENDING"
    STATUS_APPROVED = "APPROVED"
    STATUS_REJECTED = "REJECTED"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_REJECTED, "Rejected"),
    ]

    client = models.ForeignKey(
        Client, 
        on_delete=models.CASCADE,
        related_name="loans"
        )
    amount_requested = models.DecimalField(max_digits=12, decimal_places=2)
    term_months = models.PositiveIntegerField()
    loan_purpose = models.TextField(blank=True)
    daily_repayment = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    interest_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_payable = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.PROTECT, 
        related_name="loans_submitted"
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.PROTECT, 
        null=True, blank=True, 
        related_name="loans_reviewed"
    )
    decision_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Loan #{self.pk} - {self.client.first_name} - {self.status}"
    
    @property
    def total_repaid(self):
        total = sum(r.amount for r in self.repayments.all())
        return total if total is not None else Decimal("0.00")

    @property
    def balance(self):
        total_payable = self.total_payable or Decimal("0.00")
        return total_payable - self.total_repaid


class LoanRepayment(models.Model):
    loan = models.ForeignKey(
        LoanApplication, 
        on_delete=models.CASCADE,
        related_name="loan_repayments"
        )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateField(default=timezone.now)
    method = models.CharField(
        max_length=20,
        choices=[("CASH", "Cash"), ("MPESA", "M-Pesa"), ("BANK", "Bank Transfer")],
        default="CASH",
    )
    reference = models.CharField(max_length=100, blank=True, null=True)  

    def __str__(self):
        return f"Repayment {self.id} - Loan {self.loan.id} - {self.amount}"
