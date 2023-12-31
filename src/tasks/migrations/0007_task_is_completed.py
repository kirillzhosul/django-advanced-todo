# Generated by Django 4.2.4 on 2023-09-04 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_task_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='is_completed',
            field=models.BooleanField(default=False, verbose_name='Describes is task completed (by owner or another user) or not'),
        ),
    ]
