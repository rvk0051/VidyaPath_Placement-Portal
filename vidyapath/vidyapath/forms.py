from django import forms
from vidyapath_project.models import PDF

class PDFUploadForm(forms.ModelForm):
    class Meta:
        model = PDF
        fields = ['title', 'file']

from vidyapath_project.models import PlacedStudent, Company  # Import your models

class PlacedStudentForm(forms.ModelForm):
    class Meta:
        model = PlacedStudent
        fields = '__all__'  # Include all fields or specify like ['name', 'roll_no']

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'  # Include all fields or specify fields
from django import forms
from vidyapath_project.models import Registration, Resume

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['name', 'username', 'batch', 'smartCardId', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['pdf']
