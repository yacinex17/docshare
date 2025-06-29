# Generated by Django 4.2 on 2025-06-26 17:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_subject'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubSubject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subsubjects', to='accounts.subject')),
            ],
        ),
    ]
