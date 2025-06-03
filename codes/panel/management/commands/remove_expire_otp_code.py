from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from panel.models import OTP


class Command(BaseCommand):
    help = 'remove all expire otp codes'

    def handle(self, *args, **kwargs):
        expire_time  = timezone.now() - timedelta(minutes=OTP.EXPIRE_TIME)
        deleted_count, _ = OTP.objects.filter(created__lt=expire_time).delete()
        
        self.stdout.write(self.style.SUCCESS(f'{deleted_count} expired OTP(s) deleted.'))