from rest_framework.views import APIView
from rest_framework.response import Response
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
@permission_classes([IsAuthenticated])
def client_of_project(request):
    # Récupère l'objet client associé à l'utilisateur connecté
    client_id = request.user.client.id
    
    # Filtre les projets associés au client
    projects = Project.objects.filter(client=client_id)

    # Sérialise les projets
    serializer = ProjectSerializer(projects, many=True)

    # Retourne les projets sous forme de JSON
    return Response({'projects': serializer.data})




class FetchParcellesForProject(APIView):
    def get(self, request):
        project = Project.objects.get(polygon_id=3)
        parcelles = Parcelle.objects.filter(project=project.polygon_id)
        
        # Serialize data
        serializer = ParcelleSerializer(parcelles, many=True)
        
        city_data = {
            'localite_libelle': project.city.localite_libelle,
            'latitude': project.city.latitude,
            'longitude': project.city.longitude
        }

        return Response({
            'parcelles': serializer.data,
            'city': city_data,
        }, status=status.HTTP_200_OK)

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