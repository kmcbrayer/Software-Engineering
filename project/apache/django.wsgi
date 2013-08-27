import os
import sys

path='/srv/www/Django'
if path not in sys.path:
    sys.path.insert(0, '/srv/www/Django')

os.environ['DJANGO_SETTINGS_MODULE'] = 'urls_settings.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
