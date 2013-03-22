from django.db import models

class ParticipantManager(models.Manager):
    def create_participant(self, group):
        participant = self.create(completed=False, score=0, group=group)
        return participant

class Participant(models.Model):
    completed = models.BooleanField()
    score = models.DecimalField(decimal_places=5, max_digits=10)
    group = models.ForeignKey('Group')
    
    objects = ParticipantManager()
    
class Group(models.Model):
    title = models.CharField(max_length=28)
    description = models.TextField()
