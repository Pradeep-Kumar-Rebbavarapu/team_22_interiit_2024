from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Command to upload data to the server"

    def handle(self, *args, **options):
        
        pass
