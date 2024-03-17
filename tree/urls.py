from django.urls import path

from .views import index, details


urlpatterns = [
    path('', index, name='home_page'),
    path('<path:path>/', details, name='details'),
]
