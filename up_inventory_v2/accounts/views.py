from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm, CreateUserForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import CustomUser
from inventory.models import StaffRecord  

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser
from inventory.models import StaffRecord
from .forms import CreateUserForm

@login_required
def create_user_view(request):
    # Create user
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

                messages.success(request, "User created successfully.")
                return redirect('create_user')
        else:
            print("❌ FORM ERRORS:", form.errors)
            messages.error(request, "Please fix the errors in the form.")

    # Update user
    elif request.method == 'POST' and 'update_user_id' in request.POST:
        user_id = request.POST.get('update_user_id')
        user = CustomUser.objects.get(id=user_id)
        form = CreateUserForm(request.POST, instance=user)
        form.fields['staff'].queryset = StaffRecord.objects.filter(user_account_created=False) | StaffRecord.objects.filter(user_account_created=True, email=user.email)

        if form.is_valid():
            user = form.save()
            messages.success(request, "User updated successfully.")
            return redirect('create_user')
        else:
            messages.error(request, "Please fix the errors in the form.")

    # Delete user
    elif request.method == 'POST' and 'delete_user_id' in request.POST:
        user_id = request.POST.get('delete_user_id')
        try:
            user = CustomUser.objects.get(id=user_id)
            user.delete()
            messages.success(request, "User deleted successfully.")
        except CustomUser.DoesNotExist:
            messages.error(request, "User not found.")
        return redirect('create_user')

    else:
        form = CreateUserForm()
        form.fields['staff'].queryset = StaffRecord.objects.filter(user_account_created=False)

    users = CustomUser.objects.all()
    return render(request, 'signup.html', {'form': form, 'users': users})


def logout_view(request):
    logout(request)
    return redirect('login')
