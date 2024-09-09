from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse 
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from supervisor.models.project import Project
from supervisor.serializers.project import ProjectSerializer
from django.shortcuts import get_object_or_404
from supervisor.models.project import Project
from supervisor.models.parcelle import Parcelle
from supervisor.serializers.parcelle import ParcelleSerializer
from supervisor.serializers.node import NodeSerializer
from supervisor.models.node import Node



@api_view(['GET'])
def client_of_project(request):
    # Assurez-vous que l'utilisateur est authentifié
    if not request.user.is_authenticated:
        return Response({'error': 'Utilisateur non authentifié'}, status=401)

    # Récupère l'objet client associé à l'utilisateur connecté
    # Supposons que l'utilisateur a un attribut 'client' qui est une clé étrangère vers le modèle Client
    try:
        client = request.user.client  # Accès à l'objet client associé à l'utilisateur connecté
    except AttributeError:
        return Response({'error': 'Client associé à l\'utilisateur non trouvé'}, status=400)

    # Filtre les projets associés au client
    projects = Project.objects.filter(client=client)

    # Sérialise les projets
    serializer = ProjectSerializer(projects, many=True)
    
    # Retourne les projets sous forme de JSON
    return Response({'projects': serializer.data})


@api_view(['GET'])
def FetchParcellesForProject(request):
    # Récupérer le polygon_id depuis les paramètres de la requête
    polygon_id = request.query_params.get('polygon_id')

    if not polygon_id:
        return Response({"error": "polygon_id is required"}, status=400)

    # Trouver le projet correspondant à polygon_id
    project = get_object_or_404(Project, polygon_id=polygon_id)

    # Filtrer les parcelles associées à ce projet
    parcelles = Parcelle.objects.filter(project=project)

    # Sérialiser les parcelles
    serializer = ParcelleSerializer(parcelles, many=True)

    # Récupérer les informations sur la ville
    city_data = {
        'localite_libelle': project.city.localite_libelle,
        'latitude': project.city.latitude,
        'longitude': project.city.longitude
    }

    # Retourner la réponse avec les données des parcelles et de la ville
    return Response({
        'parcelles': serializer.data,
        'city_data': city_data
    })
# supervisor/views.py

class NodeListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Récupère le projet en fonction de l'identifiant et du client connecté
        project = get_object_or_404(Project, polygon_id=3, client=self.request.user.client)
        parcelles = Parcelle.objects.filter(project=project)
        nodes = Node.objects.filter(parcelle__in=parcelles)
        
        # Sérialiser les noeuds en utilisant le sérialiseur
        serializer = NodeSerializer(nodes, many=True)
        
        # Retourner la réponse en JSON
        return Response(serializer.data)