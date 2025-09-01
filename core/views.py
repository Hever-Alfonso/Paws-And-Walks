from django.shortcuts import render
from .models import Sitter
from .forms import ServiceRequestForm

def home(request):
    sitters = Sitter.objects.all()[:6]
    return render(request, 'core/home.html', {'sitters': sitters})

def about(request):
    return render(request, 'core/about.html')

def sitters_list(request):
    q = request.GET.get('q', '')
    sitters = Sitter.objects.all()
    if q:
        sitters = sitters.filter(name__icontains=q)
    return render(request, 'core/sitters_list.html', {'sitters': sitters, 'q': q})

def create_request(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'core/request_success.html')
    else:
        form = ServiceRequestForm()
    return render(request, 'core/create_request.html', {'form': form})