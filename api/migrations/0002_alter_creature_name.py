# Generated by Django 4.2.7 on 2023-12-12 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creature',
            name='name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
