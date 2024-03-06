"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""
#
# import os
#
# from django.core.wsgi import get_wsgi_application
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
#
# application = get_wsgi_application()

import os
import sys
import platform

# путь к проекту
sys.path.insert(0, '/home/p/pmercedes/varzhar-django/public_html')
# путь к фреймворку
sys.path.insert(0, '/home/p/pmercedes/varzhar-django/public_html/backend')
# путь к виртуальному окружению
python_version = ".".join(platform.python_version_tuple()[:2])
sys.path.insert(0, '/home/p/pmercedes/varzhar-django//venv/lib/python{0}/site-packages'.format(python_version))
os.environ["DJANGO_SETTINGS_MODULE"] = "backend.settings"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()