from django.urls import path, include

urlpatterns = [
      path('routes/', include('tracker.urls', namespace="tracker"))
]
