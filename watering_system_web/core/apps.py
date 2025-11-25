from django.apps import AppConfig
import sys, os

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        # start worker only when running dev server (avoid during migrations)
        if 'runserver' in sys.argv or os.environ.get('RUN_WORKER'):
            try:
                from .worker import start_background_worker
                start_background_worker()
            except Exception:
                pass
