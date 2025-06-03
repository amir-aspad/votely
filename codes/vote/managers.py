from django.utils import timezone
from django.db import models


class ActivePollManager(models.Manager):
    def get_queryset(self, **kwargs):
        now = timezone.now()

        return super().get_queryset(**kwargs).filter(
            is_active=True,
            start_time__lte=now,
            end_time__gt=now,
            type=self.model.PUBLIC
        )