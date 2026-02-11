# editor/migrations/0011_folder_topic_project_topic_alter_file_topic.py

import django.db.models.deletion
from django.db import migrations, models


def assign_general_topic(apps, schema_editor):
    Topics = apps.get_model('sms', 'Topics')
    Project = apps.get_model('webprojects', 'Project')
    Folder = apps.get_model('webprojects', 'Folder')
    File = apps.get_model('webprojects', 'File')

    # Ensure the General topic exists
    general_topic, _ = Topics.objects.get_or_create(title="General")

    # Update existing rows with null topic
    Project.objects.filter(topic__isnull=True).update(topic=general_topic)
    Folder.objects.filter(topic__isnull=True).update(topic=general_topic)
    File.objects.filter(topic__isnull=True).update(topic=general_topic)


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0007_courses_is_programming'),
        ('webprojects', '0010_alter_file_topic'),
    ]

    operations = [
        migrations.AddField(
            model_name='folder',
            name='topic',
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_DEFAULT,
                to='sms.topics'
            ),
        ),
        migrations.AddField(
            model_name='project',
            name='topic',
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_DEFAULT,
                to='sms.topics'
            ),
        ),
        migrations.AlterField(
            model_name='file',
            name='topic',
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_DEFAULT,
                to='sms.topics'
            ),
        ),

        # ✅ Data migration
        migrations.RunPython(assign_general_topic),
    ]
