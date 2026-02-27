from django.core.management.base import BaseCommand
from sms.models import Topics

class Command(BaseCommand):
    help = 'Update validation types for topics'

    def add_arguments(self, parser):
        parser.add_argument(
            '--course-id',
            type=int,
            help='Update topics for specific course ID only',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be updated without actually updating',
        )

    def handle(self, *args, **options):
        query = Topics.objects.all()
        
        if options['course_id']:
            query = query.filter(courses_id=options['course_id'])
        
        # Find topics that should be 'code' validation
        topics_with_print = query.filter(desc__icontains='print(')
        topics_with_assignments = query.filter(desc__regex=r'^\s*\w+\s*=')
        
        code_topics = (topics_with_print | topics_with_assignments).distinct()
        
        if options['dry_run']:
            self.stdout.write(self.style.WARNING(f'DRY RUN MODE - No changes will be made'))
            self.stdout.write(f'Would update {code_topics.count()} topics to "code" validation:')
            for topic in code_topics:
                self.stdout.write(f'  - [{topic.id}] {topic.title} (current: {topic.validation_type})')
        else:
            count = code_topics.update(validation_type='code')
            self.stdout.write(self.style.SUCCESS(f'Successfully updated {count} topics to "code" validation'))