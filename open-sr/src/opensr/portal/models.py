from django.db import models
from django.contrib.flatpages.models import FlatPage
from colorful.fields import RGBColorField
from ckeditor.fields import RichTextField

class ParticipantManager(models.Manager):
    def create_participant(self, group, test):
        return self.create(group=group, test=test)
    
class ResultManager(models.Manager):
    def create_result(self, primary_left_category, secondary_left_category, primary_right_category, secondary_right_category, anchor, reaction_time, correct, participant):
        return self.create(
            primary_left_category=primary_left_category, 
            secondary_left_category=secondary_left_category,
            primary_right_category=primary_right_category,
            secondary_right_category=secondary_right_category,
            anchor=anchor, 
            reaction_time=reaction_time, 
            correct=correct, 
            participant=participant
        )
    
class Test(models.Model):
    name = models.CharField(max_length=60)
    introduction_page = models.ForeignKey(FlatPage, primary_key=False, related_name='test page', null=True, blank=True)
    informed_consent_page = models.ForeignKey(FlatPage, primary_key=False, related_name='agreement page')
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
    
    def __unicode__(self):
        return self.name
    
class Group(models.Model):
    name = models.CharField(max_length=60)
    page = models.ForeignKey(FlatPage, primary_key=False, related_name='group page', null=True, blank=True)
    test = models.ForeignKey(Test)
    
    def __unicode__(self):
        return self.name
    
class Participant(models.Model):
    group = models.ForeignKey(Group, null=True)
    # TODO Is this necessary?
    test = models.ForeignKey(Test)
    objects = ParticipantManager()
    
class Trial(models.Model):
    # TODO Insert block maybe?
    primary_left_category = models.CharField(max_length=60)
    secondary_left_category = models.CharField(max_length=60)
    primary_right_category = models.CharField(max_length=60)
    secondary_right_category = models.CharField(max_length=60)
    anchor = models.CharField(max_length=32)
    reaction_time = models.DecimalField(max_digits=19, decimal_places=10)
    correct = models.BooleanField()
    participant = models.ForeignKey(Participant)
    objects = ResultManager()

class Category(models.Model):
    name = models.CharField(max_length=20) 
    color = RGBColorField()
    
    def __unicode__(self):
        return self.name
    
class Block(models.Model):
    name = models.CharField(max_length=60)
    instructions = RichTextField()
    rank = models.IntegerField()   
    practice = models.BooleanField(default=False)
    length = models.IntegerField()
    test = models.ForeignKey(Test)
    primary_right_category = models.ForeignKey(Category, related_name='primary right category')
    secondary_right_category = models.ForeignKey(Category, related_name='secondary right category', null=True, blank=True)
    primary_left_category = models.ForeignKey(Category, related_name='primary left category')
    secondary_left_category = models.ForeignKey(Category, related_name='secondary left category', null=True, blank=True)
    
    def __unicode__(self):
        return self.name

class Anchor(models.Model):
    category = models.ForeignKey(Category)
    
    class Meta:
        abstract = True
    
class ImageAnchor(Anchor):
    value = models.ImageField(upload_to="images/")
    
    def __unicode__(self):
        return self.value
    
class TextAnchor(Anchor):
    value = models.CharField(max_length=120)   
    
    def __unicode__(self):
        return self.value