# Generated by Django 4.2.7 on 2023-12-12 23:32

import api.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Creature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('max_health', models.PositiveSmallIntegerField()),
                ('defense', models.SmallIntegerField()),
                ('attack', models.SmallIntegerField()),
            ],
            bases=(api.models.UpdateMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ItemType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CombatList',
            fields=[
                ('creature', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='combat_list', serialize=False, to='api.creature')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('value', models.FloatField()),
                ('tier', models.PositiveSmallIntegerField()),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='api.itemtype')),
            ],
        ),
        migrations.CreateModel(
            name='CreatureItemCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.SmallIntegerField(default=1)),
                ('creature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='counts', to='api.creature')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.item')),
            ],
        ),
        migrations.AddField(
            model_name='creature',
            name='items',
            field=models.ManyToManyField(blank=True, through='api.CreatureItemCount', to='api.item'),
        ),
        migrations.AddField(
            model_name='creature',
            name='player',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='creature', to='api.player'),
        ),
        migrations.CreateModel(
            name='GameData',
            fields=[
                ('wins', models.PositiveSmallIntegerField(default=0)),
                ('loss', models.PositiveSmallIntegerField(default=0)),
                ('round', models.PositiveSmallIntegerField(default=0)),
                ('tier', models.PositiveSmallIntegerField(default=1)),
                ('tier_cost', models.PositiveSmallIntegerField(default=5)),
                ('gold', models.PositiveSmallIntegerField(default=3)),
                ('player', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='data', serialize=False, to='api.player')),
                ('store_list', models.ManyToManyField(blank=True, to='api.item')),
            ],
            bases=(api.models.UpdateMixin, models.Model),
        ),
    ]
