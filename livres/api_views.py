from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Livre
from .serializers import LivreSerializer

@api_view(['GET'])
def get_livres(request):
    """
    GET /api/livres/
    Récupérer tous les livres
    """
    livres = Livre.objects.all().order_by('id')
    serializer = LivreSerializer(livres, many=True)
    return Response({
        'success': True,
        'count': len(serializer.data),
        'data': serializer.data
    })

@api_view(['GET'])
def get_livre(request, id):
    """
    GET /api/livres/<id>/
    Récupérer un livre par son ID
    """
    try:
        livre = Livre.objects.get(id=id)
        serializer = LivreSerializer(livre)
        return Response({
            'success': True,
            'data': serializer.data
        })
    except Livre.DoesNotExist:
        return Response({
            'success': False,
            'error': f'Livre avec ID {id} non trouvé'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def create_livre(request):
    """
    POST /api/livres/create/
    Créer un nouveau livre
    Body JSON: {
        "titre": "Le Petit Prince",
        "auteur": "Antoine de Saint-Exupéry",
        "categorie": "Roman",
        "annee_publication": 1943,
        "quantite_disponible": 3,
        "statut": "disponible"
    }
    """
    serializer = LivreSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'success': True,
            'message': 'Livre créé avec succès',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_livre(request, id):
    """
    PUT /api/livres/update/<id>/
    Modifier un livre existant
    """
    try:
        livre = Livre.objects.get(id=id)
        serializer = LivreSerializer(livre, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Livre modifié avec succès',
                'data': serializer.data
            })
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    except Livre.DoesNotExist:
        return Response({
            'success': False,
            'error': f'Livre avec ID {id} non trouvé'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_livre(request, id):
    """
    DELETE /api/livres/delete/<id>/
    Supprimer un livre
    """
    try:
        livre = Livre.objects.get(id=id)
        titre = livre.titre
        livre.delete()
        return Response({
            'success': True,
            'message': f'Livre "{titre}" supprimé avec succès'
        }, status=status.HTTP_200_OK)
    except Livre.DoesNotExist:
        return Response({
            'success': False,
            'error': f'Livre avec ID {id} non trouvé'
        }, status=status.HTTP_404_NOT_FOUND)