# Generated by Django 4.2 on 2025-06-27 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='link',
            field=models.URLField(blank=True, help_text='Paste a link to an external document (e.g., Google Drive)', null=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='file',
            field=models.FileField(blank=True, help_text='Upload a file or provide a link below.', null=True, upload_to='documents/'),
        ),
    ]
