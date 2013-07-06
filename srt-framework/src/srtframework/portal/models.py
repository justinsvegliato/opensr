from django.db import models

class ParticipantManager(models.Manager):
    def create_participant(self, group, date_time_started):
        participant = self.create(
            datetime_started = date_time_started,
            datetime_finished = None,
            group=group
        )
        return participant

class Participant(models.Model):
    datetime_started = models.DateTimeField(default=None, null=True);
    datetime_finished = models.DateTimeField(default=None, null=True)
    
    GROUPS = (
        ('t', 'Text'),
        ('p', 'Picture'),
        ('c', 'Control')
    )   
    group = models.CharField(max_length=1, choices=GROUPS)
    
    objects = ParticipantManager()
