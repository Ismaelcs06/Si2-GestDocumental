from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, "pages/home.html")  # página pública

@login_required
def dashboard(request):
    return render(request, "pages/dashboard.html")  # página privada