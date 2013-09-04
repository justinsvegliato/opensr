from django.core.exceptions import ValidationError
from models import Test
from django.forms import (ModelForm, PasswordInput, CharField, ChoiceField, Select)
from django.forms.models import BaseInlineFormSet    
from ckeditor.widgets import CKEditorWidget
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
    
    test_choices = [("", "Select a test...")]
    test_choices.extend([(test.id, test.test_name) for test in Test.objects.all()]);
    test = ChoiceField(
        widget = Select(
            attrs = {
            'id': 'test',
            'class': 'form-control',
        }),
        choices=test_choices,
        label=''
    )

    class Meta:
        model = Test
        fields = ('test', 'password')
        
    def clean_password(self):
        test_id = self.cleaned_data['test']
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
        if not Test.objects.filter(id=self.test_id, password=password).count():
            raise ValidationError("Invalid password")
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
        widgets = {
            'content': CKEditorWidget()
        }