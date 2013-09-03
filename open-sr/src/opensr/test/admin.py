from django.contrib import admin
from django import forms
from django.contrib.flatpages.models import FlatPage
from ckeditor.widgets import CKEditorWidget
from test.admin_actions import export_as_csv
from test.models import (Test, Block, ImageStimulus, TextStimulus, ExperimentalGroup, Trial, Category, Participant)
from django.contrib.flatpages.admin import (FlatpageForm, FlatPageAdmin)

class ImageStimulusInline(admin.TabularInline):
    model = ImageStimulus
    
class TextStimulusInline(admin.TabularInline):
    model = TextStimulus 
            
class ExperimentalGroupInline(admin.StackedInline):
    model = ExperimentalGroup
    extra = 1
    
class TrialInline(admin.TabularInline):
    model = Trial
    extra = 1   
    readonly_fields = ('date', 'time', 'participant', 'block', 'practice', 
                  'primary_left_category', 'secondary_left_category', 'primary_right_category', 
                  'secondary_right_category', 'stimulus', 'correct', 'latency')
    exclude = ('test', 'experimental_group', )
    
    def has_add_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
class BlockInline(admin.StackedInline):
    model = Block
    extra = 1
    
class PageForm(FlatpageForm):
    
    class Meta:
        model = FlatPage
        widgets = {
            'content': CKEditorWidget()
        }
        
class TestForm(forms.ModelForm):
    
    class Meta:
        model = Test
        widgets = {
            'password': forms.PasswordInput(),
        }

class CategoryAdmin(admin.ModelAdmin):
    ordering = ('category_name',)
    list_display = ('category_name',)
    inlines = [
        ImageStimulusInline, TextStimulusInline
    ]
    
class TestAdmin(admin.ModelAdmin):  
    form = TestForm
    ordering = ('test_name',)
    list_display = ('test_name', 'is_active')
    inlines = [
        ExperimentalGroupInline
    ]    
    
class BlockAdmin(admin.ModelAdmin):
    ordering = ('block_name',)
    list_display = ('block_name', 'test')

class PageAdmin(FlatPageAdmin):
    form = PageForm

class ParticipantAdmin(admin.ModelAdmin):
    actions = [export_as_csv]
    ordering = ('id',)
    fields = ('test', 'experimental_group')
    list_display = ('id', 'experimental_group', 'test', 'has_completed_test')
    search_fields = ('experimental_group__group_name', 'test__test_name')
    readonly_fields = ('experimental_group', 'test')
    list_filter = ('experimental_group', 'test__test_name', 'test__is_active', 'has_completed_test')
    inlines = [
        TrialInline
    ]    
    
    def has_add_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def get_actions(self, request):
        actions = super(ParticipantAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, PageAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Block, BlockAdmin)
admin.site.register(Participant, ParticipantAdmin)