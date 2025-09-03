
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import SitterProfile, SitterService, SitterRating, SERVICE_CHOICES
from .forms import SitterProfileForm, SitterServiceForm, RatingForm

User = get_user_model()

def home(request):
    sitters = SitterProfile.objects.select_related('user').prefetch_related('services','ratings').all()
    return render(request, 'marketplace/home.html', {'sitters': sitters, 'SERVICE_CHOICES': SERVICE_CHOICES})

@login_required
def my_profile(request):
    # Role guard
    if not request.user.is_authenticated or not request.user.is_sitter:
        messages.error(request, 'Only sitters can manage a sitter profile.')
        return redirect('home')
    profile, _ = SitterProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = SitterProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado.')
            return redirect('marketplace:my_profile')
    else:
        form = SitterProfileForm(instance=profile)
    return render(request, 'marketplace/profile_form.html', {'form': form})

@login_required
def my_services(request):
    # Role guard
    if not request.user.is_authenticated or not request.user.is_sitter:
        messages.error(request, 'Only sitters can manage services.')
        return redirect('home')
    profile, _ = SitterProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = SitterServiceForm(request.POST)
        if form.is_valid():
            svc = form.save(commit=False); svc.profile = profile
            existing = SitterService.objects.filter(profile=profile, service_type=svc.service_type).first()
            if existing:
                existing.price_cop = svc.price_cop; existing.save(update_fields=['price_cop'])
                messages.success(request, 'Precio actualizado.')
            else:
                svc.save(); messages.success(request, 'Servicio agregado.')
            return redirect('marketplace:my_services')
    else:
        form = SitterServiceForm()
    services = profile.services.all()
    return render(request, 'marketplace/services_manage.html', {'form': form, 'services': services})

def sitter_detail(request, pk):
    profile = get_object_or_404(SitterProfile, pk=pk)
    my_rating = None
    if request.user.is_authenticated:
        my_rating = SitterRating.objects.filter(profile=profile, rater=request.user).first()
    ratings = profile.ratings.select_related('rater').all()
    return render(request, 'marketplace/sitter_detail.html', {'profile': profile, 'ratings': ratings, 'my_rating': my_rating})

@login_required
def rate_sitter(request, pk):
    profile = get_object_or_404(SitterProfile, pk=pk)
    # Block sitters from rating themselves
    if profile.user == request.user:
        messages.error(request, 'No puedes calificar/comentar tu propio perfil.')
        return redirect('marketplace:sitter_detail', pk=pk)
    rating = SitterRating.objects.filter(profile=profile, rater=request.user).first()
    if request.method == 'POST':
        form = RatingForm(request.POST, instance=rating)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.profile = profile; obj.rater = request.user; obj.save()
            messages.success(request, 'Calificación guardada.')
            return redirect('marketplace:sitter_detail', pk=pk)
    else:
        form = RatingForm(instance=rating)
    return render(request, 'marketplace/rate_form.html', {'form': form, 'profile': profile})

@login_required
def edit_rating(request, pk):
    rating = get_object_or_404(SitterRating, pk=pk, rater=request.user)
    if request.method == 'POST':
        form = RatingForm(request.POST, instance=rating)
        if form.is_valid():
            form.save(); messages.success(request, 'Comentario editado.')
            return redirect('marketplace:sitter_detail', pk=rating.profile.pk)
    else:
        form = RatingForm(instance=rating)
    return render(request, 'marketplace/rate_form.html', {'form': form, 'profile': rating.profile})

@login_required
def delete_rating(request, pk):
    rating = get_object_or_404(SitterRating, pk=pk, rater=request.user)
    sitter_pk = rating.profile.pk
    if request.method == 'POST':
        rating.delete(); messages.success(request, 'Comentario eliminado.')
        return redirect('marketplace:sitter_detail', pk=sitter_pk)
    return render(request, 'marketplace/rate_confirm_delete.html', {'rating': rating})


@login_required
def delete_my_profile(request):
    """Allow a sitter to permanently delete their SitterProfile.
    If the user had role 'sitter' only, we switch to 'owner' to keep account valid."""
    if not request.user.is_sitter:
        messages.error(request, 'Only sitters can delete a sitter profile.')
        return redirect('home')
    profile = SitterProfile.objects.filter(user=request.user).first()
    if request.method == 'POST':
        if profile:
            profile.delete()
        # Update role if needed
        if request.user.role == 'sitter':
            request.user.role = 'owner'
            request.user.save(update_fields=['role'])
        messages.success(request, 'Your sitter profile has been deleted.')
        return redirect('home')
    return render(request, 'marketplace/profile_confirm_delete.html', {'profile': profile})


@login_required
def delete_service(request, pk):
    if not request.user.is_sitter:
        messages.error(request, 'Only sitters can manage services.')
        return redirect('home')
    service = get_object_or_404(SitterService, pk=pk, profile__user=request.user)
    if request.method == 'POST':
        service.delete()
        messages.success(request, 'Servicio eliminado.')
        return redirect('marketplace:my_services')
    return render(request, 'marketplace/rate_confirm_delete.html', {'rating': None})
