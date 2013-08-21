from django.db import models
from django.contrib.flatpages.models import FlatPage
from colorfield.fields import ColorField

class ParticipantManager(models.Manager):
    def create_participant(self, group, test):
        return self.create(group=group, test=test)
    
class ResultManager(models.Manager):
    def create_result(self, primary_left_label, secondary_left_label, primary_right_label, secondary_right_label, anchor, reaction_time, correct, participant):
        return self.create(
            primary_left_label=primary_left_label, 
            secondary_left_label=secondary_left_label,
            primary_right_label=primary_right_label,
            secondary_right_label=secondary_right_label,
            anchor=anchor, 
            reaction_time=reaction_time, 
            correct=correct, 
            participant=participant
        )

class Confirmation(models.Model):
    title = models.CharField(max_length=32)
    body = models.TextField()
    
class Test(models.Model):
    name = models.CharField(max_length=32)
    introduction_page = models.ForeignKey(FlatPage, primary_key=False, related_name='test page', null=True, blank=True)
    informed_consent_page = models.ForeignKey(FlatPage, primary_key=False, related_name='agreement page')
    # TODO Make password field and not a char field
    password = models.CharField(max_length=32)
    is_active = models.BooleanField(default=True)
    left_key_bind = models.CharField(max_length=1)
    right_key_bind = models.CharField(max_length=1)
    survey_url = models.URLField(null=True, blank=True)
    
    TIME_INCREMENT_OPTIONS = (
        ('SECOND', 'Seconds'),
        ('DECISECOND', 'Deciseconds'),
        ('CENTISECOND', 'Centiseconds'),
        ('MILLISECOND', 'Milliseconds'),
        ('MICROSECOND', 'Microseconds')
    )   
    time_increment = models.CharField(max_length=15, choices=TIME_INCREMENT_OPTIONS)
    
    confirmation_page = models.ForeignKey(FlatPage, primary_key=False, related_name='confirmation page')
    
class Group(models.Model):
    name = models.CharField(max_length=32)
    page = models.ForeignKey(FlatPage, primary_key=False, related_name='group page', null=True, blank=True)
    test = models.ForeignKey(Test)
    
class Participant(models.Model):
    group = models.ForeignKey(Group, null=True)
    # TODO Is this necessary?
    test = models.ForeignKey(Test)
    objects = ParticipantManager()
    
class Result(models.Model):
    # TODO Insert block maybe?
    primary_left_label = models.CharField(max_length=32)
    secondary_left_label = models.CharField(max_length=32)
    primary_right_label = models.CharField(max_length=32)
    secondary_right_label = models.CharField(max_length=32)
    anchor = models.CharField(max_length=32)
    reaction_time = models.DecimalField(max_digits=19, decimal_places=10)
    correct = models.BooleanField()
    participant = models.ForeignKey(Participant)
    objects = ResultManager()

class Label(models.Model):
    name = models.CharField(max_length=20)
    color = ColorField()  
    
class Block(models.Model):
    name = models.CharField(max_length=32)
    instructions = models.TextField()
    rank = models.IntegerField()   
    practice = models.BooleanField(default=False)
    length = models.IntegerField()
    test = models.ForeignKey(Test)
    primary_right_label = models.ForeignKey(Label, related_name='primary right label')
    secondary_right_label = models.ForeignKey(Label, related_name='secondary right label', null=True, blank=True)
    primary_left_label = models.ForeignKey(Label, related_name='primary left label')
    secondary_left_label = models.ForeignKey(Label, related_name='secondary left label', null=True, blank=True)
    
class Anchor(models.Model):
    value = models.CharField(max_length=150)
    
    ANCHOR_TYPE = (
        ('AUDIO', 'Audio'),
        ('IMAGE', 'Image'),
        ('TEXT', 'Text')
    )   
    anchor_type = models.CharField(max_length=10, choices=ANCHOR_TYPE)
    
    label = models.ForeignKey(Label)