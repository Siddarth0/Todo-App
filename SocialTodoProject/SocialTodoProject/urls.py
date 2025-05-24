from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('media_app.urls', namespace='media_app')),
    path('todo/', include('todo_app.urls', namespace='todo_app')),
]
