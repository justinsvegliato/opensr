from django.forms import (
    ModelForm, PasswordInput, CharField, ChoiceField, Select
)
from django.core.exceptions import ValidationError
from models import Test

class LoginForm(ModelForm):
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
        id = self.cleaned_data['test']
        password = self.cleaned_data['password']
        if not Test.objects.filter(id=id, password=password).count():
            raise ValidationError("Invalid password")
        return password