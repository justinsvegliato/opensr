from django.core.exceptions import (ValidationError, ObjectDoesNotExist)
from models import (Test, Block)
from django.forms import (ModelForm, PasswordInput, CharField, ModelChoiceField, Select)
from django.forms.models import BaseInlineFormSet    
#from ckeditor.widgets import CKEditorWidget
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatpageForm

class IndexLoginForm(ModelForm):
    
    password = CharField(
        widget=PasswordInput(
            attrs = {
                'placeholder': 'Password',
                'id': 'password',
                'class': 'form-control',
            }), 
        label=''
    )

    test = ModelChoiceField(
        widget = Select(
            attrs = {
            'id': 'test',
            'class': 'form-control',
        }),
        queryset = Test.objects.filter(is_active=True, block__isnull=False),
        empty_label = "Select a test...",
        label = '',
    )

    class Meta:
        model = Test
        fields = ('test', 'password')
        
    def clean_password(self):
        test_id = self.cleaned_data['test'].id
        password = self.cleaned_data['password']
        if not Test.objects.filter(id=test_id, password=password).count():
            raise ValidationError("Invalid password")
        return password

class EntranceLoginForm(ModelForm):
    
    password = CharField(
        widget=PasswordInput(
            attrs={
                'placeholder': 'Password',
                'id': 'password',
                'class': 'form-control',
            }), 
        label=''
    )

    class Meta:
        model = Test
        fields = ('password',)
        
    def __init__(self, *args, **kwargs):
        self.test_id = kwargs.pop('test_id', None)
        super(EntranceLoginForm, self).__init__(*args, **kwargs)
        
    def clean_password(self):
        password = self.cleaned_data['password']
        try:
            test = Test.objects.get(id=self.test_id, password=password)
        except ObjectDoesNotExist:
            raise ValidationError("Invalid test or password")
        else:
            if not test.is_active:
                raise ValidationError("This test is not active")
        
            if Block.objects.filter(test=test).count() <= 0:
                raise ValidationError("This test has not been configured properly")
        
        return password

class AtLeastOneFormSet(BaseInlineFormSet):
    
    def clean(self):
        super(AtLeastOneFormSet, self).clean()
        non_empty_forms = 0
        for form in self:
            if form.cleaned_data:
                non_empty_forms += 1
        if non_empty_forms - len(self.deleted_forms) < 1:
            raise ValidationError("Please create at least one object")
        
class PageForm(FlatpageForm):
    
    class Meta:
        model = FlatPage
        #widgets = {
        #    'content': CKEditorWidget()
        #}
