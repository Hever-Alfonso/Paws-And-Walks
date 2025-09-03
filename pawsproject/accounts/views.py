
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from marketplace.models import SitterProfile

def signup(request):
    """Sign up with role selection. If user is/chooses sitter, we auto-create
    an empty SitterProfile so they can complete it. Then we redirect based on role."""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = form.cleaned_data['role']
            user.save()
            # Auto-create sitter profile if needed
            if user.is_sitter:
                SitterProfile.objects.get_or_create(user=user)
            login(request, user)
            messages.success(request, 'Welcome! You are registered as: %s' % user.role)
            # Redirect based on role
            if user.role == 'sitter':
                return redirect('marketplace:my_profile')
            elif user.role == 'owner':
                return redirect('requestsboard:mine')
            else:
                return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


from django.contrib.auth.decorators import login_required

@login_required
def role_redirect(request):
    """Redirect users to a sensible landing page after login based on their role."""
    user = request.user
    if user.role == 'sitter':
        return redirect('marketplace:my_profile')
    elif user.role == 'owner':
        return redirect('requestsboard:mine')
    return redirect('home')
