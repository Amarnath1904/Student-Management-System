# Generated by Django 5.1.1 on 2024-09-30 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_student_address_student_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='user_id',
            field=models.CharField(default='amar_nath', max_length=20, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='student',
            name='address',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='student',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='student',
            name='profile_image',
            field=models.ImageField(upload_to='profile_images/'),
        ),
    ]
