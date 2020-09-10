from django.forms import ModelForm
from django import forms
from .models import User

class DateInput(forms.DateInput):
    input_type = 'date'


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget= forms.PasswordInput)
    remember_me = forms.BooleanField()

class RegisterForm(ModelForm): # 繼承ModelForm
    class Meta:
        model = User # model.py
        fields= ['email', 'password', 'name', 'city', 'gender', 'date_of_birth', 'image']  # model 所有欄位，我全要。
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'input--style-5'}),
            'password': forms.PasswordInput(attrs={'class': 'input--style-5'}), # 密碼用********
            'name': forms.TextInput(attrs={'class': 'input--style-5'}),
            'date_of_birth': DateInput(attrs={'class': 'input--style-5'}),
            'city': forms.Select(attrs={'class': 'input--style-5'}),
            'gender': forms.Select(attrs={'class': 'input--style-5'}),
        }
    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user



