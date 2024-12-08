from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('',              include('homepage.urls')),
    path('professor/',    include('area_professor.urls')),
    path('aluno/',        include('area_aluno.urls')),
    path('accounts/',     include('django.contrib.auth.urls')),
    path('admin/',        admin.site.urls),
]
