from django.urls    import path
from .              import views


urlpatterns = [
    path('projC/', views.client_of_project, name='project_of_client'),
    path('fetch_parcelles/', views.FetchParcellesForProject, name='fetch_parcelles'),
    path('node/', views.NodeListView.as_view(), name='node'),

]