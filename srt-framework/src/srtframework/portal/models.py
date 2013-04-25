from django.db import models

class ParticipantManager(models.Manager):
    def create_participant(self, group):
        participant = self.create(
            iat_completed=False, 
            survey_completed=False,
            d_score=0, 
            group=group
        )
        return participant

class Participant(models.Model):
    iat_completed = models.BooleanField()
    survey_completed = models.BooleanField()
    d_score = models.DecimalField(decimal_places=5, max_digits=10)
    
    GROUPS = (
        ('t', 'Text'),
        ('p', 'Picture'),
        ('c', 'Control')
    )   
    group = models.CharField(max_length=1, choices=GROUPS)
    
    objects = ParticipantManager()
