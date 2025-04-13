from django.db import models
from datetime import datetime
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
   
class Registration(models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE)  # ✅ Link to User model
    name = models.CharField(max_length=100)
    username=models.CharField(max_length=100,default="")
    batch = models.CharField(max_length=50)
    #rollNo = models.CharField(max_length=20, unique=True)
    smartCardId = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    resume = models.FileField(upload_to='pdfs/', null=True, blank=True) # or upload_to='./' for root of media

    
    def __str__(self):
        return self.smartCardId
   # def __str__(self):
       # return self.name
      
class Login(models.Model):
    rollNo = models.CharField(max_length=20, unique=True, default="temp_roll")
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.rollNo  # ✅ Fixed __str__()
    
class Notice(models.Model):
    description = models.TextField()  # Stores the notice content
    batch = models.CharField(max_length=100)  # Add a default value
    created_at=models.DateTimeField(default=datetime.now,blank=True)
    #created_at = models.DateTimeField(auto_now_add=True)  # Stores the time & date when the notice is created

    def __str__(self):
       # return f"Notice {self.id} - {self.created_at.strftime('%d-%m-%Y %H:%M')}"
        return f"Notice for Batch {self.batch}"
    
    

       
class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    logo_url = models.CharField(max_length=500)
    details_url = models.CharField(max_length=500)
    
    def __str__(self):
        return self.name
    
class PlacedStudent(models.Model):
    student_id = models.CharField(max_length=10, primary_key=True)
    student_name = models.CharField(max_length=255)
    branch=models.CharField(max_length=200,default="Unknown")
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    placement_year = models.IntegerField()
    salary_lpa=models.FloatField()
    photo= models.ImageField(upload_to='achievers/', default='achievers/Designer_1.png',blank=True, null=True) 

    def __str__(self):
        return self.student_name
    
class PDF(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Resume(models.Model):
    student = models.ForeignKey(Registration, on_delete=models.CASCADE,related_name='resumes')
    pdf = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return f"{self.student.smartCardId} - {self.pdf.name}"
