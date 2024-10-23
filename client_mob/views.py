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
from supervisor.serializers.data import DataSerializer
from supervisor.models.data import Data


@api_view(['GET'])
def client_of_project(request):
    # Assurez-vous que l'utilisateur est authentifié
    if not request.user.is_authenticated:
        print('Utilisateur non authentifié.')
        return Response({'error': 'Utilisateur non authentifié'}, status=status.HTTP_401_UNAUTHORIZED)
    
    # Récupère l'objet client associé à l'utilisateur connecté
    try:
        client = request.user.client
        print(f'Client trouvé : {client}')
    except AttributeError:
        print('Client associé à l\'utilisateur non trouvé.')
        return Response({'error': 'Client associé à l\'utilisateur non trouvé'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Filtre les projets associés au client
    projects = Project.objects.filter(client=client)
    print(f'Projets trouvés : {projects.count()}')

    # Récupère le polygon_id depuis les paramètres de la requête
    polygon_id = request.query_params.get('polygon_id')
    print(f'polygon_id reçu : {polygon_id}')

    # Initialise city_data comme dictionnaire vide
    city_data = {}

    # Si polygon_id est fourni, filtre le projet spécifique
    if polygon_id:
        project = get_object_or_404(projects, polygon_id=polygon_id)
        print(f'Projet spécifique trouvé : {project}')
        
        # Prépare les données de la ville pour le projet spécifique
        city_data = {
            'localite_libelle': project.city.localite_libelle,
            'latitude': project.city.latitude,
            'longitude': project.city.longitude
        }
        
        # Filtre les parcelles associées à ce projet spécifique
        parcelles = Parcelle.objects.filter(project=project)
    else:
        print('Aucun polygon_id fourni. Utilisation de tous les projets associés au client.')
        parcelles = Parcelle.objects.filter(project__in=projects)

    print(f'Parcelles trouvées : {parcelles.count()}')

    # Filtre les nœuds associés aux parcelles
    nodes = Node.objects.filter(parcelle__in=parcelles)
    print(f'Nodes trouvés : {nodes.count()}')

    # Sérialise les projets, parcelles et nœuds
    projects_serializer = ProjectSerializer(projects, many=True)
    parcelles_serializer = ParcelleSerializer(parcelles, many=True)
    nodes_serializer = NodeSerializer(nodes, many=True)
    
    print('Sérialisation des données terminée.')

    # Retourne les projets, parcelles et nœuds sous forme de JSON
    return Response({
        'projects': projects_serializer.data,
        'parcelles': parcelles_serializer.data,
        'nodes': nodes_serializer.data,
        'city_data': city_data  # Ajoute city_data dans la réponse
    })


# @api_view(['GET'])
# def FetchParcellesForProject(request):
#     # Récupérer le polygon_id depuis les paramètres de la requête
#     polygon_id = request.query_params.get('polygon_id')

#     if not polygon_id:
#         return Response({"error": "polygon_id is required"}, status=400)

#     # Trouver le projet correspondant à polygon_id
#     project = get_object_or_404(Project, polygon_id=polygon_id)

#     # Filtrer les parcelles associées à ce projet
#     parcelles = Parcelle.objects.filter(project=project)

#     # Sérialiser les parcelles
#     serializer = ParcelleSerializer(parcelles, many=True)

#     # Récupérer les informations sur la ville
#     city_data = {
#         'localite_libelle': project.city.localite_libelle,
#         'latitude': project.city.latitude,
#         'longitude': project.city.longitude
#     }

#     # Retourner la réponse avec les données des parcelles et de la ville
#     return Response({
#         'parcelles': serializer.data,
#         'city_data': city_data
#     })


@api_view(['GET'])
def FetcheParcellesForProject(request):
    # Get polygon_id from request query parameters
    polygon_id = request.query_params.get('polygon_id')

    if not polygon_id:
        return Response({"error": "polygon_id is required"}, status=400)

    # Fetch the project based on polygon_id
    project = get_object_or_404(Project, polygon_id=polygon_id)

    # Filter parcelles associated with the project
    parcelles = Parcelle.objects.filter(project=project)
    
    # Filter nodes associated with these parcelles
    nodes = Node.objects.filter(parcelle__in=parcelles)

    # Filter datas associated with these nodes
    datas = Data.objects.filter(node__in=nodes)

    # Serialize parcelles, nodes, and datas
    parcelle_serializer = ParcelleSerializer(parcelles, many=True)
    node_serializer = NodeSerializer(nodes, many=True)
    data_serializer = DataSerializer(datas, many=True)  # Using DataSerializer

    # Get city information
    city_data = {
        'localite_libelle': project.city.localite_libelle,
        'latitude': project.city.latitude,
        'longitude': project.city.longitude
    }

    # Return the response with parcelles, nodes, datas, and city data
    return Response({
        'parcelles': parcelle_serializer.data,
        'nodes': node_serializer.data,
        'datas': data_serializer.data,  # Serialized data
        'city_data': city_data
    })

# class NodeListView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         # Récupère le projet en fonction de l'identifiant et du client connecté
#         project = get_object_or_404(Project, polygon_id=3, client=self.request.user.client)
#         parcelles = Parcelle.objects.filter(project=project)
#         nodes = Node.objects.filter(parcelle__in=parcelles)
        
#         # Sérialiser les noeuds en utilisant le sérialiseur
#         serializer = NodeSerializer(nodes, many=True)
        
#         # Retourner la réponse en JSON
#         return Response(serializer.data)