from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Student, FeePlan, FeeRecord
from django.core.files.storage import FileSystemStorage
from django.db.models import Sum
from .models import Student, FeeRecord
from django.contrib import messages
from django.contrib.auth.models import User, Group
import datetime




def index(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name="Admin").exists():
            return redirect('admin_dashboard')
        elif request.user.groups.filter(name="Student").exists():
            return redirect('student_dashboard')
    else:
        return redirect('login')

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.groups.filter(name="Admin").exists():
                return redirect("admin_dashboard")
            elif user.groups.filter(name="Student").exists():
                return redirect("student_dashboard")
        else:
            return HttpResponse("Invalid credentials")
    return render(request, "login.html")


def signup_view(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')  # Retrieve User ID
        name = request.POST.get('name')
        age = request.POST.get('age')
        course = request.POST.get('course')
        enrollment_date_str = request.POST.get('enrollment_date')
        address = request.POST.get('address')
        profile_image = request.FILES.get('profile_image')

        # Validation: Ensure all compulsory fields are filled in
        if not user_id or not name or not age or not course or not enrollment_date_str or not address or not profile_image:
            messages.error(request, "All fields, including user ID, address, and profile image, are required.")
            return redirect('signup')

        try:
            enrollment_date = datetime.datetime.strptime(enrollment_date_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Invalid enrollment date format. Use YYYY-MM-DD.")
            return redirect('signup')

        # Check if the user ID is unique
        if Student.objects.filter(user_id=user_id).exists():
            messages.error(request, f"User ID '{user_id}' already exists. Please choose another one.")
            return redirect('signup')



        # Handle file upload
        if profile_image:
            fs = FileSystemStorage()
            profile_image_filename = fs.save(profile_image.name, profile_image)
            profile_image_url = fs.url(profile_image_filename)

        # Create the Student record
        student = Student.objects.create(
            user_id=user_id,
            name=name,
            age=age,
            course=course,
            enrollment_date=enrollment_date,
            address=address,
            profile_image=profile_image  # Set the profile image if uploaded
        )

        # Create a corresponding User
        user = User.objects.create_user(username=user_id, password=enrollment_date_str)
        student_group, created = Group.objects.get_or_create(name='Student')
        user.groups.add(student_group)

        # Log the user in
        login(request, user)
        messages.success(
            request,
            f"Student '{name}' has been successfully added with User ID '{user_id}' and password '{enrollment_date_str}'."
        )

        return redirect('student_dashboard')

    return render(request, 'signup.html')


def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def admin_dashboard(request):
    if request.user.groups.filter(name="Admin").exists():
        # Calculate the number of students
        total_students = Student.objects.count()

        # Calculate the total revenue
        total_revenue = FeeRecord.objects.aggregate(total=Sum('amount'))['total'] or 0

        last_five_fees = FeeRecord.objects.order_by('-payment_date')[:5]

        return render(request, "admin_dashboard.html", {
            "total_students": total_students,
            "total_revenue": total_revenue,
            "last_five_fees": last_five_fees,
        })
    else:
        return HttpResponse("Unauthorized", status=401)

@login_required
def student_dashboard(request):
    if request.user.groups.filter(name="Student").exists():
        # Student-specific data and rendering
        return render(request, "student_dashboard.html")
    else:
        return HttpResponse("Unauthorized", status=401)


# admin code
@login_required
def manage_students(request):
    if request.user.groups.filter(name="Admin").exists():
        message = ""
        if request.method == "POST":
            # Manually extract user_id, name, age, course, and enrollment date from POST data
            user_id = request.POST.get('user_id')  # Extracting user_id
            name = request.POST.get('name')
            age = request.POST.get('age')
            course = request.POST.get('course', 'Default Course')  # Default or manual input
            enrollment_date_str = request.POST.get('enrollment_date')

            if user_id and name and age and enrollment_date_str:  # Basic validation
                # Convert enrollment_date_str to a datetime object
                try:
                    enrollment_date = datetime.datetime.strptime(enrollment_date_str, '%Y-%m-%d').date()
                except ValueError:
                    messages.error(request, "Invalid enrollment date format. Please use YYYY-MM-DD.")
                    return redirect('manage_students')

                # Check if a Student with the same user_id already exists
                if Student.objects.filter(user_id=user_id).exists():
                    messages.error(request, f"A student with the User ID '{user_id}' already exists. Please try another User ID.")
                else:
                    # Create and save a new Student object
                    student = Student.objects.create(
                        user_id=user_id,
                        name=name,
                        age=age,
                        course=course,
                        enrollment_date=enrollment_date
                    )

                    # Create a User with the user_id as the username and enrollment_date as the password
                    user = User.objects.create_user(
                        username=user_id,  # Use user_id as the username for the User model
                        password=enrollment_date_str  # Use the string format of enrollment_date as the password
                    )

                    # Add the user to the 'Student' group
                    student_group, created = Group.objects.get_or_create(name='Student')
                    user.groups.add(student_group)

                    messages.success(
                        request,
                        f"Student '{name}' has been successfully added with User ID '{user_id}' and password '{enrollment_date_str}'."
                    )
                    return redirect('manage_students')  # Redirect to the same page after saving

        # Fetch all students to display
        students = Student.objects.all()
        return render(request, "manage_students.html", {
            "students": students,
        })
    else:
        return HttpResponse("Unauthorized", status=401)



@login_required
def manage_fee_plans(request):
    if request.user.groups.filter(name="Admin").exists():
        message = ""
        if request.method == "POST":
            # Manually extract data from POST request
            plan_name = request.POST.get('plan_name')
            hours = request.POST.get('hours')
            per_hour_fee = request.POST.get('per_hour_fee')

            # Validate that all required fields are present
            if plan_name and hours and per_hour_fee:
                try:
                    # Convert hours and per_hour_fee to the correct data types
                    hours = int(hours)
                    per_hour_fee = float(per_hour_fee)

                    # Create and save the FeePlan
                    FeePlan.objects.create(
                        plan_name=plan_name,
                        hours=hours,
                        per_hour_fee=per_hour_fee,
                    )
                    return redirect('manage_fee_plans')  # Redirect to the same page after saving
                except ValueError:
                    message = "Invalid data format. Please enter valid numbers for hours and per hour fee."
            else:
                message = "All fields are required."

        # Fetch all fee plans to display
        fee_plans = FeePlan.objects.all()

        return render(request, "manage_fee_plans.html", {
            "fee_plans": fee_plans,
            "message": message,
        })
    else:
        return HttpResponse("Unauthorized", status=401)




@login_required
def view_fee_status(request):
    student = get_object_or_404(Student, name=request.user.username)  # Adjust field as needed
    fee_records = student.fee_records.all()
    return render(request, "view_fee_status.html", {"fee_records": fee_records})

@login_required
def manage_fees(request):
    if request.user.groups.filter(name="Admin").exists():
        message = ""
        if request.method == "POST":
            # Manually extract data from POST request
            student_id = request.POST.get('student')
            plan_id = request.POST.get('plan')
            amount = request.POST.get('amount')
            payment_date = request.POST.get('payment_date')

            # Validate that all required fields are present
            if student_id and plan_id and amount and payment_date:
                try:
                    # Fetch the related Student and FeePlan objects
                    student = Student.objects.get(id=student_id)
                    plan = FeePlan.objects.get(id=plan_id)

                    # Create and save the FeeRecord
                    FeeRecord.objects.create(
                        student=student,
                        plan=plan,
                        amount=amount,
                        payment_date=payment_date
                    )
                    return redirect('manage_fees')  # Redirect to the same page after saving
                except (Student.DoesNotExist, FeePlan.DoesNotExist):
                    message = "Invalid Student or Fee Plan selected."
            else:
                message = "All fields are required."

        # Fetch all fee records to display
        fee_records = FeeRecord.objects.all().order_by('-payment_date')
        students = Student.objects.all()
        plans = FeePlan.objects.all()

        return render(request, "manage_fees.html", {
            "fee_records": fee_records,
            "students": students,
            "plans": plans,
            "message": message,
        })
    else:
        return HttpResponse("Unauthorized", status=401)



@login_required
def student_detail(request, student_id):
    if request.user.groups.filter(name="Admin").exists():
        # Retrieve the student and their payment history
        student = get_object_or_404(Student, id=student_id)
        fee_records = FeeRecord.objects.filter(student=student).order_by('-payment_date')

        return render(request, 'student_detail.html', {
            'student': student,
            'fee_records': fee_records,
        })
    else:
        return HttpResponse("Unauthorized", status=401)