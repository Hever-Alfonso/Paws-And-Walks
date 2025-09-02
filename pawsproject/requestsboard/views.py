
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import ServiceRequest
from .forms import RequestForm

def list_requests(request):
    q = request.GET.get('q','').strip()
    items = ServiceRequest.objects.all()
    if q:
        items = items.filter(Q(title__icontains=q) | Q(description__icontains=q))
    return render(request, 'requestsboard/list.html', {'items': items, 'q': q})

@login_required
def my_requests(request):
    items = ServiceRequest.objects.filter(owner=request.user)
    return render(request, 'requestsboard/mine.html', {'items': items})

@login_required
def create_request(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            messages.success(request, '¡Solicitud publicada!')
            return redirect('requestsboard:mine')
    else:
        form = RequestForm()
    return render(request, 'requestsboard/form.html', {'form': form, 'title': 'Nueva solicitud'})

@login_required
def update_request(request, pk):
    obj = get_object_or_404(ServiceRequest, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = RequestForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Solicitud actualizada.')
            return redirect('requestsboard:mine')
    else:
        form = RequestForm(instance=obj)
    return render(request, 'requestsboard/form.html', {'form': form, 'title': 'Editar solicitud'})

@login_required
def delete_request(request, pk):
    obj = get_object_or_404(ServiceRequest, pk=pk, owner=request.user)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Solicitud eliminada.')
        return redirect('requestsboard:mine')
    return render(request, 'requestsboard/confirm_delete.html', {'obj': obj})
