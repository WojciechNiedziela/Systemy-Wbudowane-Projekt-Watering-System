import threading, time
_stop = False
_thread = None

def start_background_worker():
    global _thread, _stop
    if _thread and _thread.is_alive():
        return
    _stop = False
    _thread = threading.Thread(target=_loop, daemon=True)
    _thread.start()

def _loop():
    import time
    from django.utils import timezone
    from .models import Pomiar, Log, Ustawienia
    while not _stop:
        try:
            latest = Pomiar.objects.order_by('-data').first()
            if latest:
                delta = timezone.now() - latest.data
                minutes = int(delta.total_seconds() // 60)
                w = max(0.0, latest.wilgotnosc - minutes*10)
            else:
                w = 50.0

            # check settings - only water if auto=True
            ustaw = Ustawienia.objects.first()
            auto_on = ustaw.auto if ustaw else False

            # Auto-water only if enabled
            if auto_on and w < 30:
                w = min(100.0, w + 20)
                Log.objects.create(akcja='Auto podlewanie', szczegoly='+20%')

            Pomiar.objects.create(wilgotnosc=w)
            Log.objects.create(akcja='Auto-pomiar', szczegoly=f'{w:.1f}%')

            time.sleep(120)
        except Exception:
            time.sleep(5)
