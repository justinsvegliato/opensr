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
            'content': TinyMCE(
                attrs={
                    'cols': 100, 
                    'rows': 15
            })
        }

class LabelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [
        AnchorInline
    ]

class AnchorAdmin(admin.ModelAdmin):    
    list_display = ('value', 'anchor_type', 'label')
    
class TestAdmin(admin.ModelAdmin):    
    list_display = ('name', 'is_active')
    inlines = [
        GroupInline, BlockInline
    ]    

class PageAdmin(FlatPageAdmin):
    form = PageForm
    
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, PageAdmin)
admin.site.register(Label, LabelAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Anchor, AnchorAdmin)