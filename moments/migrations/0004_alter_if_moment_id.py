# Generated by Django 5.1.7 on 2025-07-09 03:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moments', '0003_rename_content_if_if_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='if',
            name='moment_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='if_moment', to='moments.moment'),
        ),
    ]
