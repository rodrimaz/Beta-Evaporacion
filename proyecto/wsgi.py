"""
WSGI config for proyecto project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
import sys
# add the hellodjango project path into the sys.path
sys.path.append(r'C:\inetpub\wwwroot\Beta-Evaporacion\proyecto')

# add the virtualenv site-packages path to the sys.path
sys.path.append(r'C:\Python311\Lib\site-packages')

# poiting to the project settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
