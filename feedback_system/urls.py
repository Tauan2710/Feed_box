from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from accounts.views import login_view, logout_view

def redirect_to_feedback(request):
    return redirect('enviar_feedback')

urlpatterns = [
    path('admin/', admin.site.urls),

    # login e logout (usa a view do accounts, exibe o template bonito)
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # redireciona / para enviar-feedback
    path('', redirect_to_feedback),

    # apps
    path('accounts/', include('accounts.urls')),
    path('', include('feedbacks.urls')),
    path('clima/', include('clima.urls')),
]
