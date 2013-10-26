from django.db import models
from django.contrib.flatpages.models import FlatPage
from colorful.fields import RGBColorField
from ckeditor.fields import RichTextField
from django.forms import (fields, TextInput)

class MultipleTextField(fields.MultiValueField):
    widget = TextInput

    def __init__(self, *args, **kwargs):
        all_fields = (
            fields.CharField(),
            fields.CharField(),
        )
        super(MultipleTextField, self).__init__(all_fields, *args, **kwargs)

    def compress(self, data_list):
        return None
        
class ParticipantManager(models.Manager):
    def create_participant(self, experimental_group, test):
        return self.create(experimental_group=experimental_group, test=test)
    
class TrialManager(models.Manager):
    def create_result(self, test, experimental_group, block, practice, primary_left_category, secondary_left_category, 
        primary_right_category, secondary_right_category, stimulus, latency, correct, participant):
        return self.create(
            test=test,
            experimental_group=experimental_group,
            block=block,
            practice=practice,
            primary_left_category=primary_left_category, 
            secondary_left_category=secondary_left_category,
            primary_right_category=primary_right_category,
            secondary_right_category=secondary_right_category,
            stimulus=stimulus, 
            latency=latency, 
            correct=correct, 
            participant=participant
        )
    
class Test(models.Model):
    test_name = models.CharField(max_length=60, unique=True)
    introduction_page = models.ForeignKey(FlatPage, primary_key=False, related_name='test page', null=True, blank=True)
    informed_consent_page = models.ForeignKey(FlatPage, primary_key=False, related_name='agreement page')
    password = models.CharField(max_length=32, verbose_name='passcode')
    is_active = models.BooleanField(default=True)
    left_key_bind = models.CharField(max_length=1)
    right_key_bind = models.CharField(max_length=1)
    # survey_url = models.URLField(null=True, blank=True)    
    survey_url = MultipleTextField()
    
    confirmation_page = models.ForeignKey(FlatPage, primary_key=False, related_name='confirmation page')
        
    def __unicode__(self):
        return self.test_name
    
class ExperimentalGroup(models.Model):
    group_name = models.CharField(max_length=60)
    page = models.ForeignKey(FlatPage, primary_key=False, related_name='experimental group page', null=True, blank=True)
    test = models.ForeignKey(Test)
    
    def __unicode__(self):
        return self.group_name
    
class Participant(models.Model):
    experimental_group = models.ForeignKey(ExperimentalGroup, null=True)
    test = models.ForeignKey(Test)
    has_completed_test = models.BooleanField(default=False)
    objects = ParticipantManager()
    
    class Meta:
        verbose_name = "result"
    
    def __unicode__(self):
        return "Participant"
    
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=20, unique=True) 
    color = RGBColorField()
    
    class Meta:
        verbose_name_plural = "categories"
    
    def __unicode__(self):
        return self.category_name
    
class Block(models.Model):
    block_name = models.CharField(max_length=60, unique=True)
    instructions = RichTextField()
    order = models.IntegerField()   
    practice = models.BooleanField(default=False)
    number_of_stimuli = models.IntegerField(verbose_name='Number of trials')
    test = models.ForeignKey(Test)
    primary_right_category = models.ForeignKey(Category, related_name='primary right category')
    secondary_right_category = models.ForeignKey(Category, related_name='secondary right category', null=True, blank=True)
    primary_left_category = models.ForeignKey(Category, related_name='primary left category')
    secondary_left_category = models.ForeignKey(Category, related_name='secondary left category', null=True, blank=True)
    
    def __unicode__(self):
        return self.block_name

class Stimulus(models.Model):
    id = models.AutoField(primary_key=True, editable=True)
    category = models.ForeignKey(Category)
    
    class Meta:
        abstract = True
    
class ImageStimulus(Stimulus):
    value = models.ImageField(upload_to="images/")
    
    def __unicode__(self):
        return self.value
    
class TextStimulus(Stimulus):  
    value = models.CharField(max_length=60) 
    
    def __unicode__(self):
        return self.value
    
class Trial(models.Model):
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)
    test = models.ForeignKey(Test)
    participant = models.ForeignKey(Participant)
    experimental_group = models.CharField(max_length=60)
    block = models.CharField(max_length=60)
    practice = models.BooleanField()
    primary_left_category = models.CharField(max_length=60)
    secondary_left_category = models.CharField(max_length=60)
    primary_right_category = models.CharField(max_length=60)
    secondary_right_category = models.CharField(max_length=60)
    stimulus = models.CharField(max_length=120)
    latency = models.DecimalField(max_digits=20, decimal_places=2)
    correct = models.BooleanField()
    objects = TrialManager()