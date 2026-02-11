# Generated manually to add topic to File and populate existing rows
from django.db import migrations, models
from sms.models import Topics

def populate_file_topic(apps, schema_editor):
    File = apps.get_model('webprojects', 'File')
    TopicsModel = apps.get_model('sms', 'Topics')

    # Ensure "General" topic exists
    general_topic, _ = TopicsModel.objects.get_or_create(title="General")

    # Update existing File records to use general_topic
    File.objects.filter(topic__isnull=True).update(topic=general_topic)

class Migration(migrations.Migration):

    dependencies = [
        ('webprojects', '0014_populate_default_topic'),  # adjust if needed
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='topic',
            field=models.ForeignKey(
                to='sms.Topics',
                on_delete=models.SET_NULL,
                null=True,
                blank=True,
            ),
        ),
        migrations.RunPython(populate_file_topic, reverse_code=migrations.RunPython.noop),
    ]
