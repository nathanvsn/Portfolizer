# Generated by Django 5.1.2 on 2024-10-22 22:46

import taggit.managers
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolios', '0006_resource_file_type'),
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]