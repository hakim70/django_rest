from django.urls    import path
from .              import views


urlpatterns = [
    path('projC/', views.client_of_project, name='project_of_client'),
    path('fetch-parcelles/', views.FetchParcellesForProject.as_view(), name='fetch_parcelles_for_project'),
    path('node/', views.NodeListView.as_view(), name='node'),

]