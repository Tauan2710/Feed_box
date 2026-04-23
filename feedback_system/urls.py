from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect

def redirect_to_feedback(request):
    return redirect('enviar_feedback')

urlpatterns = [
    path('admin/', admin.site.urls),

    # login e logout
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # redireciona / para enviar-feedback
    path('', redirect_to_feedback),

    # apps
    path('', include('feedbacks.urls')),
    path('clima/', include('clima.urls')),

    
]
