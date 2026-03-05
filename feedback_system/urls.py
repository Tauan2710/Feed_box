from turtle import home
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def redirect_dashboard(request):
    return redirect('dashboard')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_dashboard),
    path('', include('feedbacks.urls')),
]
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect

def redirect_dashboard(request):
    return redirect('dashboard')

urlpatterns = [
    path('admin/', admin.site.urls),

    # login e logout
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # redireciona /
    path('', redirect_dashboard),

    # app feedbacks
    path('', include('feedbacks.urls')),
    path('', include('clima.urls')),
    path('', home, name='home'),
    path('clima/', include('clima.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    
]
