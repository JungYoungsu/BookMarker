import os
import sys
from django.core.wsgi import get_wsgi_application

sys.path.append('/home/ubuntu/bm_web/bm_web')
os.environ['DJANGO_SETTINGS_MODULE'] = 'bm_web.settings'

application = get_wsgi_application()
