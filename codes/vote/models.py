from django.contrib.auth import get_user_model
from django.db import models

# import from vote app
from .managers import ActivePollManager

User = get_user_model()


class Poll(models.Model):
    class Meta:
        ordering = ('-created', )


    PUBLIC = 'public'
    PRIVATE = 'private'
    POLL_TYPE_CHOICES = [
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'),
    ]

    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='polls')
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True, null=True)

    # datetime field
    created = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    is_active = models.BooleanField(default=True)
    type = models.CharField(max_length=10, choices=POLL_TYPE_CHOICES, default=PUBLIC)


    # set config for model
    objects = models.Manager()
    config = ActivePollManager()

    def __str__(self):
        return self.title[:50]
    

    def is_open(self):
        """
        Check if the poll is currently open for voting.

        The poll is open if the current time is between start_time and end_time.

        Returns:
            bool: True if the poll is open, False otherwise.
        """
        from django.utils.timezone import now
        return self.start_time <= now() <= self.end_time
    

    def can_vote(self, user):
        """
        Check if the given user is allowed to vote in this poll.

        Conditions for voting:
        - The poll must be active.
        - The poll must be currently open (start and end times are valid).
        - If the poll is private, the user must be in PollAllowedUser for this poll.

        Returns:
            bool: True if the user can vote, False otherwise.
        """
        if not self.is_active or not self.is_open():
            return False
    
        if self.type == Poll.PRIVATE:
            if not PollAllowedUser.objects.filter(poll=self, user=user).exists():
                return False
        return True
    

class PollAllowedUser(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='poll_allowed')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='poll_allowed')

    def __str__(self):
        return f'{self.user} allowed in {self.poll}'


class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=120)
    votes_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.text
    

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='votes')
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name='votes')
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'poll')
    
    def __str__(self):
        return f'{self.user} -> {self.choice}'