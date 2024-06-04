

import datetime
from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

class AutoLogoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            return

        now = datetime.datetime.now()
        last_activity = request.session.get('last_activity')

        if last_activity:
            elapsed_time = (now - datetime.datetime.strptime(last_activity, '%Y-%m-%d %H:%M:%S.%f')).total_seconds()
            if elapsed_time > settings.SESSION_COOKIE_AGE:
                logout(request)
                return redirect('login')  # Redirige al usuario a la página de inicio de sesión
        
        # Actualizar la última actividad del usuario en la sesión
        request.session['last_activity'] = str(now)
