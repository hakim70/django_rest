from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .serializers import  LoginSerializer



class LoginView(APIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
       
        return Response({'token': token.key},  status=status.HTTP_200_OK)
        
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Pour les tokens d'authentification
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
        except Token.DoesNotExist:
            pass  # Token already deleted or never created

        # Pour les tokens JWT
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                # Blacklist the refresh token
                RefreshToken(refresh_token).blacklist()
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)
