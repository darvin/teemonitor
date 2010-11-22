from django.core.management.base import BaseCommand, CommandError
from teeworlds_monitor.models import Server

class Command(BaseCommand):
    args = ''
    help = 'Refreshes all Teeworlds servers'

    def handle(self, *args, **options):
        Server.objects.refresh()
        self.stdout.write('Successfully refreshed servers\n')
