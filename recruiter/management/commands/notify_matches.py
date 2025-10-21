from django.core.management.base import BaseCommand
from recruiter.views import notify_recruiters_of_new_matches

class Command(BaseCommand):
    help = 'Notify recruiters about new candidate matches for their saved searches'

    def handle(self, *args, **options):
        self.stdout.write('Checking for new candidate matches...')
        
        try:
            notify_recruiters_of_new_matches()
            self.stdout.write(
                self.style.SUCCESS('Successfully checked for new matches and sent notifications')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error occurred while checking for matches: {e}')
            )
