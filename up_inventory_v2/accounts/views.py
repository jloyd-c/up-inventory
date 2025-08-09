from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm, CreateUserForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import CustomUser
from inventory.models import StaffRecord
from inventory.utils import log_action
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from django.db import models

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
   
            log_action(
                request,
                'login',
                'User',
                user.id,
                f"User {user.email} logged in successfully"
            )
            return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def create_user_view(request):
    query = request.GET.get("q", "")
    start_date = request.GET.get("start_date", "")
    end_date = request.GET.get("end_date", "")
    page = request.GET.get('page', 1)

    users = CustomUser.objects.all().order_by('-id')


    if query:
        users = users.filter(
            models.Q(email__icontains=query) | 
            models.Q(full_name__icontains=query)
        )
    
 
    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            users = users.filter(date_joined__date__range=[start_date, end_date])
        except ValueError:
            messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")
    elif start_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            users = users.filter(date_joined__date__gte=start_date)
        except ValueError:
            messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")
    elif end_date:
        try:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            users = users.filter(date_joined__date__lte=end_date)
        except ValueError:
            messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")


    if request.method == 'POST' and 'create_user' in request.POST:
        form = CreateUserForm(request.POST)
        form.fields['staff'].queryset = StaffRecord.objects.filter(user_account_created=False)

        if form.is_valid():
            staff = form.cleaned_data.get('staff')
            email = form.cleaned_data.get('email')
            full_name = form.cleaned_data.get('full_name')

            if staff:
                email = staff.email
                full_name = staff.full_name

            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "A user with this email already exists.")
            else:
                user = form.save(commit=False)
                user.email = email
                user.full_name = full_name
                user.is_active = True
                user.save()

                if staff:
                    staff.user_account_created = True
                    staff.save()

            
                log_action(
                    request,
                    'user_create',
                    'User',
                    user.id,
                    f"Created user account for {email} with staff {staff.full_name if staff else 'N/A'}"
                )
                messages.success(request, "User created successfully.")
                return redirect(f"{request.path}?{request.GET.urlencode()}")
        else:
           
            log_action(
                request,
                'user_create',
                'User',
                None,
                f"Failed user creation attempt with errors: {form.errors}"
            )
            messages.error(request, "Please fix the errors in the form.")


    elif request.method == 'POST' and 'update_user_id' in request.POST:
        user_id = request.POST.get('update_user_id')
        user = get_object_or_404(CustomUser, id=user_id)
        form = CreateUserForm(request.POST, instance=user)
        form.fields['staff'].queryset = StaffRecord.objects.filter(user_account_created=False) | StaffRecord.objects.filter(user_account_created=True, email=user.email)

        if form.is_valid():
            old_email = user.email
            old_staff = user.staff
            user = form.save()
            
            
            log_details = f"Updated user account {old_email} to {user.email}"
            if old_staff != user.staff:
                log_details += f", staff association changed from {old_staff.full_name if old_staff else 'None'} to {user.staff.full_name if user.staff else 'None'}"
            
            log_action(
                request,
                'user_update',
                'User',
                user.id,
                log_details
            )
            messages.success(request, "User updated successfully.")
            return redirect(f"{request.path}?{request.GET.urlencode()}")
        else:
           
            log_action(
                request,
                'user_update',
                'User',
                user.id,
                f"Failed update attempt with errors: {form.errors}"
            )
            messages.error(request, "Please fix the errors in the form.")


    elif request.method == 'POST' and 'delete_user_id' in request.POST:
        user_id = request.POST.get('delete_user_id')
        try:
            user = CustomUser.objects.get(id=user_id)
            email = user.email
            user.delete()
            
           
            log_action(
                request,
                'user_delete',
                'User',
                user_id,
                f"Deleted user account {email}"
            )
            messages.success(request, "User deleted successfully.")
        except CustomUser.DoesNotExist:
           
            log_action(
                request,
                'user_delete',
                'User',
                None,
                f"Attempted to delete non-existent user with ID {user_id}"
            )
            messages.error(request, "User not found.")
        return redirect(f"{request.path}?{request.GET.urlencode()}")

    else:
        form = CreateUserForm()
        form.fields['staff'].queryset = StaffRecord.objects.filter(user_account_created=False)

    # Add pagination
    paginator = Paginator(users, 15)  
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'signup.html', {
        'form': form,
        'users': users,
        'query': query,
        'start_date': start_date,
        'end_date': end_date,
    })

def logout_view(request):
    if request.user.is_authenticated:

        log_action(
            request,
            'logout',
            'User',
            request.user.id,
            f"User {request.user.email} logged out"
        )
    logout(request)
    return redirect('login')