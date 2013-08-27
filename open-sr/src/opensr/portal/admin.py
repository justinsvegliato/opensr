from django.contrib import admin
from django import forms
from django.contrib.flatpages.models import FlatPage
from ckeditor.widgets import CKEditorWidget
from portal.models import (
    Test, Block, ImageAnchor, TextAnchor, Group, Category
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
        GroupInline, BlockInline
    ]    

class PageAdmin(FlatPageAdmin):
    form = PageForm
    
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, PageAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Test, TestAdmin)