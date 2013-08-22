from django.core.exceptions import ValidationError
from models import Test
from django.forms import (
    ModelForm, PasswordInput, CharField, ChoiceField, Select
)

class IndexLoginForm(ModelForm):
    password = CharField(
        widget=PasswordInput(
            attrs={
                'placeholder': 'Password',
                'id': 'password'
            }), 
        label=''
    )
    
    test_choices = [("", "Select a test...")]
    test_choices.extend([(test.id, test.name) for test in Test.objects.all()]);
    test = ChoiceField(
        widget = Select(attrs={'id': 'test'}),
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
                'id': 'password'
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