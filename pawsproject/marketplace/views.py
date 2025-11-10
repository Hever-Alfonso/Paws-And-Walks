# marketplace/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.http import JsonResponse
from .models import (
    SitterProfile, SitterService, SitterRating, Message, Appointment, SERVICE_CHOICES
)
from .forms import SitterProfileForm, SitterServiceForm, RatingForm
import json
from datetime import datetime

User = get_user_model()


def home(request):
    sitters = SitterProfile.objects.select_related('user').prefetch_related('services', 'ratings').all()
    return render(request, 'marketplace/home.html', {'sitters': sitters, 'SERVICE_CHOICES': SERVICE_CHOICES})


def sitter_detail(request, pk):
    sitter_profile = get_object_or_404(SitterProfile, pk=pk)
    ratings = sitter_profile.ratings.select_related('rater').all()
    my_rating = None

    # Contexto base
    context = {
        'sitter': sitter_profile,
        'ratings': ratings,
        'my_rating': my_rating,
        'messages': [],
        'appointments': [],
    }

    # Si el usuario está logueado, cargar chat y citas
    if request.user.is_authenticated:
        my_rating = SitterRating.objects.filter(profile=sitter_profile, rater=request.user).first()

        # Cargar mensajes
        if request.user == sitter_profile.user:
            messages_qs = Message.objects.filter(
                sitter_profile=sitter_profile,
                receiver=sitter_profile.user
            )
        else:
            messages_qs = Message.objects.filter(
                sitter_profile=sitter_profile,
                sender__in=[request.user, sitter_profile.user],
                receiver__in=[request.user, sitter_profile.user]
            )

        # Cargar citas (como owner o como sitter)
        appointments = Appointment.objects.filter(
            sitter_profile=sitter_profile,
            owner=request.user
        ) | Appointment.objects.filter(
            sitter_profile=sitter_profile,
            sitter=request.user
        )

        context.update({
            'messages': messages_qs,
            'appointments': appointments,
            'my_rating': my_rating,
        })

        # Manejo de POST (solo si está logueado)
        if request.method == 'POST':
            # --- Mensaje de chat ---
            if 'message' in request.POST:
                content = request.POST.get('message', '').strip()
                if content:
                    Message.objects.create(
                        sender=request.user,
                        receiver=sitter_profile.user,
                        sitter_profile=sitter_profile,
                        content=content
                    )
                    messages.success(request, "Mensaje enviado.")
                return redirect('marketplace:sitter_detail', pk=pk)

            # --- Agendar cita ---
            elif 'appointment_date' in request.POST:
                date_str = request.POST.get('appointment_date')
                notes = request.POST.get('notes', '')
                if date_str:
                    try:
                        # Parsear string del input datetime-local
                        # Ejemplo: "2025-11-15T01:29"
                        cleaned = date_str.replace('Z', '+00:00')
                        appointment_date = datetime.fromisoformat(cleaned)

                        # 🔧 ARREGLO: si viene naive, lo volvemos aware
                        if timezone.is_naive(appointment_date):
                            appointment_date = timezone.make_aware(
                                appointment_date,
                                timezone.get_current_timezone()
                            )

                        # Ahora sí se puede comparar con timezone.now() (ambos aware)
                        if appointment_date <= timezone.now():
                            messages.error(request, "La fecha de la cita debe ser futura.")
                        else:
                            Appointment.objects.create(
                                owner=request.user,
                                sitter=sitter_profile.user,
                                sitter_profile=sitter_profile,
                                date=appointment_date,
                                notes=notes
                            )
                            messages.success(request, "Cita agendada exitosamente.")
                    except ValueError:
                        messages.error(request, "Formato de fecha inválido.")
                return redirect('marketplace:sitter_detail', pk=pk)

    return render(request, 'marketplace/sitter_detail.html', context)


# --- Vistas protegidas (requieren login) ---
@login_required
def my_profile(request):
    if not request.user.is_sitter:
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
    if not request.user.is_sitter:
        messages.error(request, 'Only sitters can manage services.')
        return redirect('home')
    profile, _ = SitterProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = SitterServiceForm(request.POST)
        if form.is_valid():
            svc = form.save(commit=False)
            svc.profile = profile
            existing = SitterService.objects.filter(profile=profile, service_type=svc.service_type).first()
            if existing:
                existing.price_cop = svc.price_cop
                existing.save(update_fields=['price_cop'])
                messages.success(request, 'Precio actualizado.')
            else:
                svc.save()
                messages.success(request, 'Servicio agregado.')
            return redirect('marketplace:my_services')
    else:
        form = SitterServiceForm()
    services = profile.services.all()
    return render(request, 'marketplace/services_manage.html', {'form': form, 'services': services})


# --- Calificaciones ---
@login_required
def rate_sitter(request, pk):
    profile = get_object_or_404(SitterProfile, pk=pk)
    if profile.user == request.user:
        messages.error(request, 'No puedes calificar tu propio perfil.')
        return redirect('marketplace:sitter_detail', pk=pk)
    rating = SitterRating.objects.filter(profile=profile, rater=request.user).first()
    if request.method == 'POST':
        form = RatingForm(request.POST, instance=rating)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.profile = profile
            obj.rater = request.user
            obj.save()
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
            form.save()
            messages.success(request, 'Comentario editado.')
            return redirect('marketplace:sitter_detail', pk=rating.profile.pk)
    else:
        form = RatingForm(instance=rating)
    return render(request, 'marketplace/rate_form.html', {'form': form, 'profile': rating.profile})


@login_required
def delete_rating(request, pk):
    rating = get_object_or_404(SitterRating, pk=pk, rater=request.user)
    sitter_pk = rating.profile.pk
    if request.method == 'POST':
        rating.delete()
        messages.success(request, 'Comentario eliminado.')
        return redirect('marketplace:sitter_detail', pk=sitter_pk)
    return render(request, 'marketplace/rate_confirm_delete.html', {'rating': rating})


# --- Eliminación ---
@login_required
def delete_my_profile(request):
    if not request.user.is_sitter:
        messages.error(request, 'Only sitters can delete a sitter profile.')
        return redirect('home')
    profile = SitterProfile.objects.filter(user=request.user).first()
    if request.method == 'POST':
        if profile:
            profile.delete()
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
    return render(request, 'marketplace/service_confirm_delete.html', {'service': service})


# --- Chat AJAX ---
@login_required
def send_message_ajax(request, pk):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        sitter_profile = get_object_or_404(SitterProfile, pk=pk)
        try:
            data = json.loads(request.body)
            content = data.get('message', '').strip()
            if content:
                msg = Message.objects.create(
                    sender=request.user,
                    receiver=sitter_profile.user,
                    sitter_profile=sitter_profile,
                    content=content
                )
                return JsonResponse({
                    'status': 'ok',
                    'message': {
                        'content': msg.content,
                        'sender': msg.sender.username,
                        'timestamp': msg.timestamp.strftime('%H:%M')
                    }
                })
        except Exception as e:
            return JsonResponse({'status': 'error', 'msg': str(e)}, status=400)
    return JsonResponse({'status': 'error'}, status=400)
