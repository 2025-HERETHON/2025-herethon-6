# Generated by Django 5.1.7 on 2025-07-07 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('image_id', models.AutoField(primary_key=True, serialize=False)),
                ('moment_id', models.IntegerField(blank=True, null=True)),
                ('image_url', models.URLField()),
                ('image_name', models.CharField(max_length=255)),
            ],
        ),
    ]
