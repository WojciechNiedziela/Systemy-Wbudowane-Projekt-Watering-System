from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.utils import timezone
from .models import Pomiar, Log, Ustawienia

def _current():
    latest = Pomiar.objects.order_by('-data').first()
    if not latest:
        return 50.0
    delta = timezone.now() - latest.data
    minutes = int(delta.total_seconds() // 60)
    return max(0.0, latest.wilgotnosc - minutes*10)

def dashboard(request):
    ustaw = Ustawienia.objects.first()
    if not ustaw:
        ustaw = Ustawienia.objects.create(auto=False)
    return render(request, 'dashboard.html',{
        'pomiary': Pomiar.objects.order_by('-data')[:20],
        'logi': Log.objects.order_by('-data')[:20],
        'current': _current(),
        'settings': ustaw
    })

def pomiary(request):
    return render(request,'pomiary.html',{
        'wszystkie': Pomiar.objects.order_by('-data')
    })

def api_dane(request):
    qs = Pomiar.objects.order_by('-data')[:10][::-1]
    return JsonResponse({
        'labels':[p.data.strftime('%H:%M:%S') for p in qs],
        'wilgotnosc':[p.wilgotnosc for p in qs]
    })

def podlej(request):
    w = min(100.0, _current()+10)
    Pomiar.objects.create(wilgotnosc=w)
    Log.objects.create(akcja='Podlewanie', szczegoly='+10%')
    return redirect('/')

def obroc(request):
    Log.objects.create(akcja='Obróć')
    return redirect('/')

def ustaw_auto_toggle(request):
    ustaw = Ustawienia.objects.first()
    if not ustaw:
        ustaw = Ustawienia.objects.create(auto=False)
    ustaw.auto = not ustaw.auto
    ustaw.save()
    Log.objects.create(akcja='Przełączono tryb auto', szczegoly=f'auto={ustaw.auto}')
    return redirect('/')

def zmierz(request):
    w = _current()
    Pomiar.objects.create(wilgotnosc=w)
    Log.objects.create(akcja='Pomiar', szczegoly=f'{w:.1f}%')
    return redirect('/')
