from django.core.management.base import BaseCommand
from authentication.models import User

class Command(BaseCommand):
    help = 'Create an admin user'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(username='admin', email='admin@example.com', password='admin123', role='admin')
            self.stdout.write(self.style.SUCCESS('Admin user created!'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists.'))