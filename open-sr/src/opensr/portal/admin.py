from django.contrib import admin
from django import forms
from django.contrib.flatpages.models import FlatPage
from ckeditor.widgets import CKEditorWidget
from portal.actions import export_as_csv
from portal.models import (
    Test, Block, ImageAnchor, TextAnchor, Group, Trial, Category, Participant
)
from django.contrib.flatpages.admin import (
    FlatpageForm, FlatPageAdmin
)

class ImageAnchorInline(admin.TabularInline):
    model = ImageAnchor 
    
class TextAnchorInline(admin.TabularInline):
    model = TextAnchor 
            
class GroupInline(admin.StackedInline):
    model = Group
    extra = 1
    
class TrialInline(admin.TabularInline):
    model = Trial
    extra = 1   
    readonly_fields = ('date', 'time', 'test', 'participant', 'group', 'block', 'practice', 
                  'primary_left_category', 'secondary_left_category', 'primary_right_category', 
                  'secondary_right_category', 'anchor', 'correct', 'latency')
    
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
    list_display = ('name',)
    inlines = [
        ImageAnchorInline, TextAnchorInline
    ]
    
class TestAdmin(admin.ModelAdmin):  
    form = TestForm
    list_display = ('name', 'is_active')
    inlines = [
        GroupInline
    ]    
    
class BlockAdmin(admin.ModelAdmin):
    list_display = ('name', 'test')

class PageAdmin(FlatPageAdmin):
    form = PageForm

class ParticipantAdmin(admin.ModelAdmin):
    actions = [export_as_csv]
    readonly_fields = ('group', 'test')
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
