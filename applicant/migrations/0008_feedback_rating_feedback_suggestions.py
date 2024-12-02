# Generated by Django 5.1.3 on 2024-12-02 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicant', '0007_remove_applicant_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='rating',
            field=models.IntegerField(blank=True, choices=[(1, 'Poor'), (2, 'Fair'), (3, 'Good'), (4, 'Very Good'), (5, 'Excellent')], null=True),
        ),
        migrations.AddField(
            model_name='feedback',
            name='suggestions',
            field=models.TextField(blank=True, null=True),
        ),
    ]
