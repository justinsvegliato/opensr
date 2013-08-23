from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
from tinymce.widgets import TinyMCE
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
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'instructions':
            kwargs['widget'] = TinyMCE(attrs={'cols': 100, 'rows': 15})
        return super(BlockInline, self).formfield_for_dbfield(db_field, **kwargs)
    
class PageForm(FlatpageForm):
    class Meta:
        model = FlatPage
        widgets = {
            'content': TinyMCE(
                attrs={
                    'cols': 100, 
                    'rows': 15
            })
        }

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [
        ImageAnchorInline, TextAnchorInline
    ]
    
class TestAdmin(admin.ModelAdmin):    
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