from django.urls import path, include


urlpatterns = [
    path('auth/', include('api.v1.auth.urls')),
    path('task/', include('api.v1.task.urls')),
]