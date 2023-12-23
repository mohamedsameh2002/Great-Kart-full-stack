from django import forms
from .models import Accounts,UserProfile


class RegistrationForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter Password',
        'class':'form-control',
        }))
    conf_password=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'confirm Password',
        'class':'form-control',
        }))
        
    class Meta:
        model=Accounts
        fields=['first_name','last_name','phone_numper','email','password']
    def __init__(self,*args, **kwargs) :
        super(RegistrationForm,self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder']='Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder']='Enter Last Name'
        self.fields['email'].widget.attrs['placeholder']='Enter Email'
        self.fields['phone_numper'].widget.attrs['placeholder']='Enter Phone Numper'
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
    def clean(self):
        clean_data=super(RegistrationForm,self).clean()
        password=clean_data.get('password')
        conf_password=clean_data.get('conf_password')
        if password != conf_password:
            raise forms.ValidationError(
                'password dos not mach!'
            )




class UserForm (forms.ModelForm):
    class Meta :
        model=Accounts
        fields=['first_name','last_name','phone_numper']
    def __init__(self,*args, **kwargs) :
        super(UserForm,self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'


class UserProfileForm (forms.ModelForm):
    profile_pictuer=forms.ImageField(required=False,error_messages={'invaile':("Image File Only")},widget=forms.FileInput)
    class Meta :
        model=UserProfile
        fields=['address_line_1','address_line_2','city','state','country','profile_pictuer']
    def __init__(self,*args, **kwargs) :
        super(UserProfileForm,self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'

