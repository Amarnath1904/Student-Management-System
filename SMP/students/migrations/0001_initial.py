# Generated by Django 5.0.3 on 2024-08-25 09:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FeePlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_name', models.CharField(max_length=100)),
                ('hours', models.IntegerField()),
                ('per_hour_fee', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('course', models.CharField(max_length=100)),
                ('enrollment_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='FeeRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('payment_date', models.DateTimeField(blank=True, null=True)),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fee_plan_records', to='students.feeplan')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fee_records', to='students.student')),
            ],
        ),
    ]
