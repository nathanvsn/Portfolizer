# Generated by Django 5.1 on 2024-10-22 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='project_images/'),
        ),
    ]
