from django.contrib import admin
from students.models import Student, FeeRecord, FeePlan


admin.site.register(Student)
admin.site.register(FeeRecord)
admin.site.register(FeePlan)
