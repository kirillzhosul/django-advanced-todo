# Generated by Django 4.2.4 on 2023-09-04 01:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_task_asignee_id_alter_task_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='asignee_id',
            new_name='asignee',
        ),
    ]
