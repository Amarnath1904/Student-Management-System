from django.db import models
from numpy.ma.core import minimum


class Student(models.Model):
    user_id = models.CharField(max_length=20, unique=True, null=False, blank=False)  # User ID field
    name = models.CharField(max_length=100, null=False, blank=False)
    age = models.IntegerField()
    course = models.CharField(max_length=100)
    enrollment_date = models.DateField()
    profile_image = models.ImageField(upload_to='profile_images/', null=False, blank=False)
    address = models.TextField(null=False, blank=False)
    phone_number = models.CharField(max_length=12, null=False, blank=False)

    def __str__(self):
        return f"{self.user_id} - {self.name}"


class FeePlan(models.Model):
    plan_name = models.CharField(max_length=100)
    hours = models.IntegerField()
    per_hour_fee = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.plan_name} - {self.hours} hr(s) @ {self.per_hour_fee} per hour"

class FeeRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fee_records')
    plan = models.ForeignKey(FeePlan, on_delete=models.CASCADE, related_name='fee_plan_records')
    status = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    payment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.payment_date} - {self.status}"
