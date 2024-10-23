from django.urls    import path
from .              import views


urlpatterns = [
    path('projC/', views.client_of_project, name='project_of_client'),
    path('fetch_parcelles/', views.FetcheParcellesForProject, name='fetch_parcelles'),
]