# Generated by Django 4.2.7 on 2023-12-13 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_creature_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='creature',
            name='level',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
