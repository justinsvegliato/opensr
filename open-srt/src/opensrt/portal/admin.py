from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
from tinymce.widgets import TinyMCE
from portal.models import (
    Test, Block, Anchor, Group, Label
)
from django.contrib.flatpages.admin import (
    FlatpageForm, FlatPageAdmin
)

class AnchorInline(admin.TabularInline):
    model = Anchor 
    
class LabelAdmin(admin.ModelAdmin):
    inlines = [
        AnchorInline
    ]
    
admin.site.register(Label, LabelAdmin)
        
class GroupInline(admin.StackedInline):
    model = Group
    extra = 1
    
class BlockInline(admin.StackedInline):
    model = Block
    extra = 1
    
class TestAdmin(admin.ModelAdmin):    
    inlines = [
        GroupInline, BlockInline
    ]    
    
admin.site.register(Test, TestAdmin)

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

class PageAdmin(FlatPageAdmin):
    form = PageForm
    
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, PageAdmin)