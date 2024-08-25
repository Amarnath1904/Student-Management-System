from django.db import models
from django.utils import timezone

class Student(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    age = models.IntegerField()
    course = models.CharField(max_length=100)
    enrollment_date = models.DateField()

    def __str__(self):
        return f"{self.id} - {self.name}"

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
