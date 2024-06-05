import datetime
from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

class AutoLogoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            return

        session_key = f'{request.user.pk}_{request.META["REMOTE_ADDR"]}'
        now = datetime.datetime.now()
        last_activity = request.session.get('last_activity')

        if last_activity:
            elapsed_time = (now - datetime.datetime.strptime(last_activity, '%Y-%m-%d %H:%M:%S.%f')).total_seconds()
            if elapsed_time > settings.SESSION_COOKIE_AGE or request.session.get('session_key') != session_key:
                logout(request)
                return redirect('signin')  # Redirige al usuario a la página de inicio de sesión

        # Actualizar la última actividad del usuario en la sesión
        request.session['last_activity'] = str(now)
        request.session['session_key'] = session_key


