# Generated by Django 5.0.4 on 2024-05-09 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animals', '0009_animal_responsible_employee_animalclass_time_create_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='animal',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='animals_images'),
        ),
    ]
