"""
WSGI config for libralink project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

from whitenoise import WhiteNoise
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'libralink.settings')

application = get_wsgi_application()


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

application = get_wsgi_application()
application = WhiteNoise(application, root=os.path.join(
    os.path.dirname(os.path.dirname(__file__)), 'media'), prefix='/media/')
