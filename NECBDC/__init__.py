from .celery import app as celery_app  

__all__ = ('celery_app',)

# celery -A NECBDC worker -l info