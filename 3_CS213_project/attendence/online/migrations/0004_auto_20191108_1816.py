# Generated by Django 2.2.6 on 2019-11-08 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online', '0003_auto_20191108_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendence',
            name='t',
            field=models.DateTimeField(),
        ),
    ]
