from django.db import models
from django.contrib.flatpages.models import FlatPage
from colorful.fields import RGBColorField
from ckeditor.fields import RichTextField
from django.forms import (fields, TextInput)
from django.db.models import signals
from sortedm2m.fields import SortedManyToManyField
        
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
        
class StimuliOrderManager(models.Manager):
    def create_stimuli_order(self, block):
        return self.create(block=block)
    
class Test(models.Model):
    test_name = models.CharField(max_length=60, unique=True)
    introduction_page = models.ForeignKey(FlatPage, primary_key=False, related_name='test page', null=True, blank=True)
    informed_consent_page = models.ForeignKey(FlatPage, primary_key=False, related_name='agreement page')
    password = models.CharField(max_length=32, verbose_name='passcode')
    is_active = models.BooleanField(default=True)
    left_key_bind = models.CharField(max_length=1)
    right_key_bind = models.CharField(max_length=1)
    survey_url = models.URLField(null=True, blank=True)    
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
        
class Stimulus(models.Model):
    id = models.AutoField(primary_key=True, editable=True)
    category = models.ForeignKey(Category)
    word = models.CharField(max_length=60, null=True, blank=True) 
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    help_text = "A stimulus can either have a word or a image but not both at the same time."
    
    def __unicode__(self):
        stimulus_name = self.word if self.word else self.image
        return "%s (%s)" % (stimulus_name, self.category.category_name)
        
class Block(models.Model):
    block_name = models.CharField(max_length=60, unique=True)
    instructions = RichTextField()
    order = models.IntegerField()
    practice = models.BooleanField(default=False)
    number_of_stimuli = models.IntegerField(verbose_name='Number of trials')
    intertrial_interval = models.IntegerField(verbose_name='Intertrial Interval (in milliseconds)', null=True, blank=True)
    trial_interval = models.IntegerField(verbose_name='Trial Interval (in milliseconds)', null=True, blank=True)
    test = models.ForeignKey(Test)
    primary_left_category = models.ForeignKey(Category, related_name='primary left category')
    secondary_left_category = models.ForeignKey(Category, related_name='secondary left category', null=True, blank=True)
    primary_right_category = models.ForeignKey(Category, related_name='primary right category')
    secondary_right_category = models.ForeignKey(Category, related_name='secondary right category', null=True, blank=True)
    
    def __unicode__(self):
        return self.block_name
        
class StimuliOrder(models.Model):
    id = models.AutoField(primary_key=True, editable=True)
    stimuli = SortedManyToManyField(Stimulus, primary_key=False, null=True, blank=True, verbose_name="Order (drag and drop)")
    random_order = models.BooleanField(default=True)
    block = models.OneToOneField(Block, null=True, blank=True)
    
    objects = StimuliOrderManager()
    
    class Meta:
        verbose_name_plural = "Block Stimuli Order"
        
    def __unicode__(self):
        return self.block.test.test_name + " - " + self.block.block_name
    
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
    
def create_stimuli_ordering(sender, instance, created, **kwargs):
    signals.post_save.disconnect(create_stimuli_ordering, sender=Block)
    
    block = Block.objects.get(block_name=instance.block_name)
    category_ids = []
    category_ids.append(block.primary_left_category_id)
    category_ids.append(block.primary_right_category_id)
    if not block.primary_left_category_id is None:
        category_ids.append(block.secondary_left_category_id)
    if not block.secondary_right_category_id is None:
        category_ids.append(block.secondary_right_category_id)
    stimuli = Stimulus.objects.filter(category_id__in=category_ids)
    
    hasCategoriesChanged = False
    stimuli_orders = StimuliOrder.objects.filter(block=block)
    if stimuli_orders.count() > 0:
        old_category_ids = set()
        old_stimuli_ids = set()
        for stimulus in stimuli_orders[0].stimuli.get_queryset():
            old_category_ids.add(stimulus.category.id)
            old_stimuli_ids.add(stimulus.id)
        
        new_category_ids = set(filter(None, category_ids))
        new_stimuli_ids = set()    
        for stimulus in stimuli:
            new_stimuli_ids.add(stimulus.id)
            
        hasCategoriesChanged = old_category_ids != new_category_ids # or new_stimuli_ids != old_stimuli_ids
        
        if hasCategoriesChanged:
            stimuli_orders[0].delete()
    else:
        hasCategoriesChanged = True
        
    if hasCategoriesChanged:
        stimuli_order = StimuliOrder.objects.create_stimuli_order(block=block)
        stimuli_order.save()
        
        stimuli_order.stimuli = stimuli
        stimuli_order.save()
    
    signals.post_save.connect(create_stimuli_ordering, sender=Block)
    
signals.post_save.connect(create_stimuli_ordering, sender=Block)
