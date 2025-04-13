from django.shortcuts import render, redirect
from vidyapath_project.models import Registration
from vidyapath_project.models import Notice
from vidyapath_project.models import Login
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout  # ✅ This is the correct import
from django.core.files.storage import FileSystemStorage


#from django.contrib.auth.models import User
#from django.contrib.auth import get_user_model
#from django.contrib.auth import login

def home(request):
    all_members=Notice.objects.all()
    return render(request, 'home.html',{'all':all_members})

def register(request):
    return render(request, 'register.html')


def contact(request):
    return render(request,'contact.html')

def aboutus(request):
    return render(request,'aboutus.html')

def adminlogin(request):
    return render(request,'adminlogin.html')

def admindashboard(request):
    all_members=Registration.objects.all()
    return render(request,'admindashboard.html',{'all':all_members})

def notice(request):
    all_notices = Notice.objects.all()
    all_batches = Registration.objects.values_list('batch', flat=True).distinct()  # Fetch distinct batch values

    if request.method == "POST":
        description = request.POST.get("description")
        batch = request.POST.get("batch")

        if description and batch:
            notice = Notice.objects.create(description=description, batch=batch)

            # Fetch students from the selected batch
            students = Registration.objects.filter(batch=batch)
            recipient_list = [student.email for student in students]

            if recipient_list:
                send_mail(
                    subject="New Notice Published",
                    message=f"A new notice has been posted for Batch {batch}:\n\n{description}",
                    from_email="shreyauttam97@gmail.com",
                    recipient_list=recipient_list,
                    fail_silently=False,
                )
                messages.success(request, f"Notice added and email sent to Batch {batch} successfully!")
            else:
                messages.warning(request, f"Notice added, but no students found for Batch {batch}.")

            return redirect("notice")

    return render(request, "notice.html", {'all': all_notices, 'all_batches': all_batches})

from django.contrib.auth.models import User
def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        batch = request.POST['batch']
        smart_card_id = request.POST['smartCardId']
        email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']
        resume = request.FILES.get('resume')  # Get the uploaded file

        if password == confirmpassword:
            try:
                # Create a User instance
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,  # `create_user` hashes the password automatically
                )
                user.first_name = name
                user.save()

                # Create a Registration instance linked to this user
                registration = Registration.objects.create(
                    name=name,
                    username=username,
                    batch=batch,
                    smartCardId=smart_card_id,
                    email=email,
                    password=make_password(password)  # Hash password before saving
                )

                if resume:
                    fs = FileSystemStorage(location='media/pdfs/')  # Save in 'media/pdfs/'
                    filename = fs.save(resume.name, resume)
                    registration.resume = f'pdfs/{filename}' #store the file path relative to media folder
                    registration.save()

                # Authenticate and login the user
                authenticated_user = authenticate(username=username, password=password)

                if authenticated_user:
                    login(request, authenticated_user)
                    messages.success(request, "Registration successful! You are now logged in.")
                    return redirect("dashboard")

            except Exception as e:
                print("Error creating user:", e)
                messages.error(request, "User creation failed. Try again.")
                return redirect('register')

        else:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

    return render(request, "register.html")
        
            
        # Hash the password before saving it
        #hashed_password = make_password(password)

        # Save data to the database
''' new_user=Registration(
            name=name,
            batch=batch,
            rollNo=roll_no,
            smartCardId=smart_card_id,
            email=email,
            password=hashed_password  # Store hashed password
        )
        new_user.save()
        messages.success(request, "Registration successful! You can now log in.")
        return redirect('signin')  # Redirect to the home page after registration

    return render(request, 'register.html')'''
    
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.shortcuts import render, redirect

'''def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']  # ✅ New Username Field
        batch = request.POST['batch']
        roll_no = request.POST['rollNo']
        smart_card_id = request.POST['smartCardId']
        email = request.POST['email']
        password = request.POST['password']

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken. Choose another one.")
            return render(request, 'register.html')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'register.html')

       # ✅ Use create_user() instead of create()
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password  # No need to hash manually
        )
        # Save additional data in a separate model (if required)
        new_user = Registration(
             user=user,  # ✅ Link to Django User model
            name=name,
            batch=batch,
            rollNo=roll_no,
            smartCardId=smart_card_id,
            email=email
        )
        new_user.save()

        messages.success(request, "Registration successful! You can now log in.")
        return redirect('signin')

    return render(request, 'register.html')
'''

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def signin(request):
    if request.user.is_authenticated:
        return redirect('student_dashboard')  # 🔁 Use actual dashboard route name

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        if not username or not password:
            messages.error(request, "Username and Password are required.")
            response = render(request, "login.html")
        else:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                response = redirect("student_dashboard")  # 🔁 Use correct route
            else:
                messages.error(request, "Invalid username or password.")
                response = render(request, "login.html")
    else:
        response = render(request, 'login.html')

    # ✅ Add security headers to all responses
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response


def update_notice(request,id):
    mem=Notice.objects.get(id=id)
    return render(request,'update_notice.html',{'mem':mem})

def delete1(request,id):
    mem1=Notice.objects.get(id=id)
    mem1.delete()
    return redirect('notice')

def delete(request,id):
    mem=Registration.objects.get(id=id)
    mem.delete()
    return redirect('admindashboard')

def update_notice1(request,id):
    x=request.POST['description']
    mem=Notice.objects.get(id=id)
    mem.description=x
    mem.save()
    return redirect('notice')

def chatbot(request):
    return render(request, 'chatbot.html')

def placement(request):
    return render(request, 'placement.html')

def learningdev(request):
    return render(request, 'learningdev.html')

def placementg(request):
    return render(request, 'placementg.html')


    
    
    
from django.contrib.auth import logout
from django.shortcuts import redirect   
def signout(request):
    logout(request)
    response = redirect('home')
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

#def placement_stats(request):
 #   return render(request, 'placement_stats.html')

from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count, Max
from vidyapath_project.models import PlacedStudent, Company
from django.conf import settings
from vidyapath_project.utils import calculate_salary_distribution  # Import the function
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Count, Max
import json
from .forms import PlacedStudentForm, CompanyForm
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist

from vidyapath_project.models import PlacedStudent, Company
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from vidyapath_project.utils import calculate_salary_distribution  # Import the function
def placement_stats(request):
    """Render the placement stats page."""
    return render(request, 'placement_stats.html')

def get_chart_data(request):
    """Fetch placement statistics filtered by company and branch."""
    
    selected_company = request.GET.get('company', None)
    selected_branch = request.GET.get('branch', None)

    # Default company: the one offering the highest salary
    highest_salary_company = PlacedStudent.objects.order_by('-salary_lpa').first()
    default_company = highest_salary_company.company.name if highest_salary_company else None

    # Get all companies for the dropdown
    all_companies = list(Company.objects.values_list('name', flat=True).distinct())

    # Get all branches and ensure "All Branches" is the first option
    all_branches = ["All Branches"] + list(PlacedStudent.objects.values_list('branch', flat=True).distinct())

    # If no company is selected, use the default one
    if not selected_company:
        selected_company = default_company

    # Apply filters
    filters = {'company__name': selected_company} if selected_company else {}

    # Ensure proper filtering when selecting a specific branch
    if selected_branch and selected_branch != "All Branches":
        filters['branch'] = selected_branch  

    # Query to get placement data
    company_placement_data = list(
        PlacedStudent.objects.filter(**filters)
        .values('placement_year')
        .annotate(students_placed=Count('student_id'))
        .order_by('placement_year')
    )

    return JsonResponse({
        'company_placement_data': company_placement_data,
        'companies': all_companies,
        'branches': all_branches,  # Now includes "All Branches"
        'default_company': default_company,
        'selected_company': selected_company,
        'selected_branch': selected_branch if selected_branch else "All Branches"
    })


def get_salary_distribution(request):
    """Fetch salary distribution dynamically with 10 LPA steps."""
    selected_branch = request.GET.get('branch', None)
    selected_year = request.GET.get('year', None)

    # Default filters
    filters = {}
    if selected_branch:
        filters['branch'] = selected_branch
    if selected_year:
        filters['placement_year'] = selected_year

    # Get available branches & years
    all_branches = list(PlacedStudent.objects.values_list('branch', flat=True).distinct())
    all_years = list(PlacedStudent.objects.values_list('placement_year', flat=True).distinct())

    # Fixed Salary Ranges (0-10, 10-20, ...)
    salary_ranges = [(f"{i} - {i+10} LPA", i, i+10) for i in range(0, 100, 10)]  # 0-10, 10-20, ... till 100 LPA

    salary_distribution = []
    for label, min_range, max_range in salary_ranges:
        count = PlacedStudent.objects.filter(**filters, salary_lpa__gte=min_range, salary_lpa__lt=max_range).count()
        salary_distribution.append({'salary_range': label, 'students_count': count})

    total_placed_students = sum(item['students_count'] for item in salary_distribution)

    return JsonResponse({
        'salary_distribution': salary_distribution,
        'total_placed_students': total_placed_students,
        'branches': all_branches,
        'years': all_years
    })


def get_top_achievers(request):
    top_achievers = (
        PlacedStudent.objects.values('placement_year')
        .annotate(max_salary=Max('salary_lpa'))
        .order_by('-placement_year')
    )

    achievers_data = []
    for achiever in top_achievers:
        student = PlacedStudent.objects.filter(
            placement_year=achiever['placement_year'],
            salary_lpa=achiever['max_salary']
        ).first()

        if student:
            if student.photo:
               photo_url = student.photo.url
            else:
                photo_url = f"{settings.MEDIA_URL}achievers/Designer(1).png"

            achievers_data.append({
                'year': student.placement_year,
                'student_name': student.student_name,
                'company': student.company.name,
                'salary_lpa': student.salary_lpa,
                'branch': student.branch,
                'photo': photo_url,
            })

    return JsonResponse({'top_achievers': achievers_data})


#ADMIN SIDE PLACEMENT STATS
def admin_entry(request):
    return render(request, "admin_entry.html")

def get_companies(request):
    """Returns a list of all existing companies."""
    companies = list(Company.objects.values("id", "name"))
    return JsonResponse({"companies": companies}, safe=False)

@csrf_exempt
def add_company(request):
    """Adds a new company to the database."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("Received Data:", data)  # Debugging Step

            company = Company.objects.create(
                name=data.get("name", "").strip(),
                logo_url=data.get("logo_url", "").strip(),
                details_url=data.get("details_url", "").strip()
            )

            print("Company Created:", company)  # Debugging Step
            return JsonResponse({"message": "Company added successfully!", "id": company.id}, status=201)

        except Exception as e:
            print("Error in add_company:", str(e))  # Debugging Step
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def add_student(request):
    """Adds a new placed student to the database."""
    if request.method == "POST":
        try:
            student_id = request.POST.get("student_id")
            student_name = request.POST.get("student_name")
            company_id = request.POST.get("company")
            placement_year = int(request.POST.get("placement_year"))
            salary_lpa = float(request.POST.get("salary_lpa"))
            branch = request.POST.get("branch")
            photo = request.FILES.get("photo")

            company = get_object_or_404(Company, id=company_id)

            student = PlacedStudent.objects.create(
                student_id=student_id,
                student_name=student_name,
                company=company,
                placement_year=placement_year,
                salary_lpa=salary_lpa,
                branch=branch,
                photo=photo
            )

            return JsonResponse({"message": "Student added successfully!", "student_id": student.student_id}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def delete_student(request, student_id):
    if request.method == "POST":
        student = get_object_or_404(PlacedStudent, student_id=student_id)
        student.delete()
        return JsonResponse({"success": True, "message": "Student deleted successfully"})
    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)


def get_students(request):
    placement_year = request.GET.get("placement_year", None)
    student_id = request.GET.get("student_id", None)

    students = PlacedStudent.objects.all()

    if placement_year:
        students = students.filter(placement_year=placement_year)

    if student_id:
        students = students.filter(student_id=student_id)

    students_data = [
        {
            "student_id": student.student_id,
            "student_name": student.student_name,
            "company": student.company.name if student.company else "Not Placed",
            "placement_year": student.placement_year,
            "salary_lpa": student.salary_lpa,
            "branch": student.branch,
            "photo": student.photo.url if student.photo else f"{settings.MEDIA_URL}achievers/Designer_1.png"
        }
        for student in students
    ]

    return JsonResponse({"students": students_data}, safe=False)
    
def students_view(request):
    return render(request, 'admin_entry.html')


@csrf_exempt
def delete_company(request, id):
    if request.method == "POST":
        company = get_object_or_404(Company, id=id)
        company.delete()
        return JsonResponse({"success": True, "message": "Company deleted successfully"})
    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)




#from django.contrib.auth.decorators import login_required

#def login_view(request):
#    if request.user.is_authenticated:
#       return redirect('dashboard')  # Redirect if already logged in
#   return render(request, 'login.html')

#@login_required(login_url='signin')
#def dashboard(request):
    
#    response = render(request, 'dashboard.html')
#    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
#   response['Pragma'] = 'no-cache'
#  response['Expires'] = '0'
#   return response
  



from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User

# ✅ Define the default admin email and password
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "admin12345"  # 🔹 Use a strong password in production!

def adminlogin(request):
    if request.method == "POST":
        email = request.POST.get("email").strip()
        password = request.POST.get("password").strip()

        # ✅ Check if the entered email and password match the default admin credentials
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            # ✅ Create a dummy admin user session
            user, created = User.objects.get_or_create(username="admin", email=ADMIN_EMAIL)
            login(request, user)  # Logs in the admin user
            return redirect("admindashboard")  # ✅ Redirect to Admin Dashboard
        
        else:
            messages.error(request, "Invalid email or password!")  # ✅ Show error message

    return render(request, "adminlogin.html")  # ✅ Render the login page
   
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import FileResponse
from vidyapath_project.models import PDF
from .forms import PDFUploadForm

def pdf_manager(request):
    # Handle the upload form
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('pdf_manager')
    else:
        form = PDFUploadForm()

    # Handle the list of PDFs
    pdfs = PDF.objects.all()
    paginator = Paginator(pdfs, 10)  # Show 10 PDFs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'pdf_manager.html', {'form': form, 'page_obj': page_obj})

def pdf_manager(request):
    return render(request, 'pdf_manager.html')

def download_pdf(request, pdf_id):
    pdf = PDF.objects.get(id=pdf_id)
    return FileResponse(pdf.file.open(), as_attachment=True)



'''def resume_list(request):
    resumes = Registration.objects.values('name', 'username', 'email', 'resume')  # Fetch only resume data
    for resume in resumes:
            print(resume.resume.url)  # Print the URL
    return render(request, 'resume_list.html', {'resumes': resumes})'''

def resume_list(request):
    resumes = Registration.objects.values('name', 'username', 'email', 'resume')
    return render(request, 'resume_list.html', {'resumes': resumes, 'MEDIA_URL': settings.MEDIA_URL})



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from vidyapath_project.models import Resume, Registration
from .forms import ResumeUploadForm
import os
from django.conf import settings

@login_required
def student_dashboard(request):
    user = request.user
    student = get_object_or_404(Registration, smartCardId=user.username)  # Assuming smartCardId == username

    resumes = Resume.objects.filter(student=student).order_by('-uploaded_at')
    form = ResumeUploadForm()

    if request.method == 'POST':
        if 'upload_resume' in request.POST:
            form = ResumeUploadForm(request.POST, request.FILES)
            if form.is_valid():
                if resumes.count() >= 5:
                    oldest_resume = resumes.last()
                    if oldest_resume:
                        oldest_resume.pdf.delete()
                        oldest_resume.delete()

                new_resume = form.save(commit=False)
                new_resume.student = student
                new_resume.save()
                messages.success(request, "Resume uploaded successfully.")
                return redirect('student_dashboard')

        elif 'delete_resume' in request.POST:
            resume_id = request.POST.get('resume_id')
            resume = get_object_or_404(Resume, id=resume_id, student=student)
            resume.pdf.delete()
            resume.delete()
            messages.success(request, "Resume deleted successfully.")
            return redirect('student_dashboard')

        elif 'edit_resume' in request.POST:
            resume_id = request.POST.get('resume_id')
            resume = get_object_or_404(Resume, id=resume_id, student=student)
            form = ResumeUploadForm(request.POST, request.FILES, instance=resume)
            if form.is_valid():
                form.save()
                messages.success(request, "Resume updated successfully.")
                return redirect('student_dashboard')

    context = {
        'form': form,
        'resumes': resumes,
        'student': student,
    }
    return render(request, 'student_dashboard.html', context)

@login_required
def download_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, student__smartCardId=request.user.username)
    resume_path = os.path.join(settings.MEDIA_ROOT, resume.pdf.name)
    return FileResponse(open(resume_path, 'rb'), as_attachment=True, filename=os.path.basename(resume_path))
from django.contrib.auth import logout

def signout(request):
    logout(request)
    return redirect('signin')
from django.shortcuts import get_object_or_404, redirect
from vidyapath_project.models import Resume  # Make sure Resume model is imported
from django.contrib.auth.decorators import login_required

@login_required
def delete_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    resume.file.delete()  # Deletes the file from media folder
    resume.delete()       # Deletes the object from DB
    return redirect('student_dashboard')  # Redirect to your dashboard view
