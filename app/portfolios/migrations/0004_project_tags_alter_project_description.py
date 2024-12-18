# Generated by Django 5.1.2 on 2024-10-22 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolios', '0003_project_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='tags',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(blank=True, max_length=400, null=True),
        ),
    ]
