from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, CreateUserForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import CustomUser
from inventory.models import StaffRecord  # adjust if needed

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('staff')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def create_user_view(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            staff = form.cleaned_data.get('staff')
            email = form.cleaned_data.get('email')
            full_name = form.cleaned_data.get('full_name')

            if staff:
                email = staff.email
                full_name = staff.full_name

            user = CustomUser(
                email=email,
                full_name=full_name,
                is_active=True
            )
            user.set_password(form.cleaned_data['password1'])
            user.save()

            if staff:
                staff.user_account_created = True
                staff.save()

            return redirect('dashboard')
    else:
        form = CreateUserForm()
    return render(request, 'signup.html', {'form': form})





def logout_view(request):
    logout(request)
    return redirect('login')
