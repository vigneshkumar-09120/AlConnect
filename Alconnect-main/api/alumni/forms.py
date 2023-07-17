from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


from .models import Alumni,Category,Job,Higherstudies
from base.models import Document

from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django import forms
from django.core.exceptions import ValidationError
import re
def validate_name(value):
    if not re.match(r'^[a-zA-Z ]+$', value):
        raise ValidationError('Name can only contain alphabets and spaces.')
def rvce_email_validator(value):
    if not value.endswith('@rvce.edu.in'):
        raise ValidationError('RVCE Email should end with @rvce.edu.in')    

class AlumniCreationForm(forms.ModelForm):
    
    def clean_user(self):
        email = self.cleaned_data['email']
        user, _ = User.objects.get_or_create(email=email)
        alumni = Group.objects.get(name='alumni')
        user.username = email[:len(email)-12]
        user.set_password('anteater')
        user.groups.add(alumni)
        user.save()
        return user

    user = forms.ModelChoiceField(queryset=User.objects.all(), required=False)
    name = forms.CharField(validators=[validate_name], widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "Enter the name"}))
    phone = forms.CharField(validators=[RegexValidator(r'^\d+$', 'Enter a valid phone number.')],widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "Enter the phone number"}))
    rv_email = forms.EmailField(validators=[rvce_email_validator],widget=forms.EmailInput(
        attrs={"class": "form-control", "placeholder": "Enter the rv email"}))

    class Meta:
        model = Alumni
        fields = ['name', 'usn', 'phone', 'rv_email', 'email', 'branch', 'year_joined', 'year_passed', 'user']
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter the name"}),
            'usn': forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter the USN"}),
            'phone': forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter the phone number"}),
            'rv_email': forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter the RV email"}),
            'email': forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter the email"}),
            'branch': forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter the branch"}),
            'year_joined': forms.DateInput(attrs={'type': 'date',"class": "form-control"}),
            'year_passed': forms.DateInput(attrs={'type':'date' ,"class": "form-select"}),
        }


class AlumniUploadForm(forms.ModelForm):
    def validate_file(file):
        if not file.name.endswith('.csv'):
            raise ValidationError("Only csv file format supported!")
        return file

    file = forms.FileField(validators=[validate_file], widget=forms.FileInput(
        attrs={"class": "form-control"}))

    class Meta:
        model = Document
        fields = ["name", "file"]

class Catform(forms.ModelForm):
    class Meta:
        model=Category
        fields= '__all__'
        widgets = {
            'Category': forms.Select(attrs={"class": "form-control"}),
            'description':forms.Textarea(attrs={"class": "form-control", "placeholder": "Enter  short description of ur present status "}),
            
           
        }
class Jobform(forms.ModelForm):
    class Meta:
        model=Job
        fields= '__all__'
        widgets = {
            'company_name': forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter the company name"}),
            'role': forms.Select(attrs={"class": "form-control", "placeholder": "Enter the role"}),
            'salary': forms.NumberInput(attrs={"class": "form-control", "placeholder": "Enter the salary"}),
            'location': forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter the Job location"}),
           
        }

class Highform(forms.ModelForm):
    class Meta:
        model=Higherstudies
        fields= '__all__'
        widgets = {
            'college_name': forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter the college name"}),
            'location': forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter the Institute country"}),
            'specialization': forms.Select(attrs={"class": "form-control", "placeholder": "Enter the specialization"}),
            'degree': forms.Select(attrs={"class": "form-control", "placeholder": "Enter the degree"}),
            'yearofgrad': forms.DateInput(attrs={ "type":'date',"class": "form-control", "placeholder": "select date of graduation (expected)"}),
        }