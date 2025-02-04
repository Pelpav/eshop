# Generated by Django 5.1.4 on 2024-12-19 19:57

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-created_at', 'name']},
        ),
        migrations.AddField(
            model_name='product',
            name='active',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AddField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='likes',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
