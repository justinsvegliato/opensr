from django.contrib import admin
from django import forms
from django.contrib.flatpages.models import FlatPage
from ckeditor.widgets import CKEditorWidget
from portal.admin_actions import export_as_csv
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
    readonly_fields = ('date', 'time', 'participant', 'block', 'practice', 
                  'primary_left_category', 'secondary_left_category', 'primary_right_category', 
                  'secondary_right_category', 'anchor', 'correct', 'latency')
    exclude = ('test', 'group', )
    
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
        ImageAnchorInline, TextAnchorInline
    ]
    
class TestAdmin(admin.ModelAdmin):  
    form = TestForm
    ordering = ('test_name',)
    list_display = ('test_name', 'is_active')
    inlines = [
        GroupInline
    ]    
    
class BlockAdmin(admin.ModelAdmin):
    ordering = ('block_name',)
    list_display = ('block_name', 'test')

class PageAdmin(FlatPageAdmin):
    form = PageForm

class ParticipantAdmin(admin.ModelAdmin):
    actions = [export_as_csv]
    ordering = ('id',)
    fields = ('test', 'group')
    list_display = ('id', 'group', 'test')
    search_fields = ('group__group_name', 'test__test_name')
    readonly_fields = ('group', 'test')
    list_filter = ('group', 'test__test_name', 'test__is_active')
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
