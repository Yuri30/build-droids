from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import  permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import status


from ..models import Anunciante, Endereco
from .serializers import AnuncianteSerializer, EnderecoSerializer


class AnuncianteViewSet(viewsets.ModelViewSet):
    serializer_class = AnuncianteSerializer
    queryset = Anunciante.objects.all()

    #@authentication_classes([BasicAuthentication, SessionAuthentication])
    #@permission_classes([IsAuthenticated, IsAdminUser])
    def list(self, request):
        queryset = Anunciante.objects.all()
        serializer = AnuncianteSerializer(queryset, many=True)
        return Response(serializer.data)
    
    #@authentication_classes([BasicAuthentication, SessionAuthentication])
    #@permission_classes([IsAuthenticated])
    def retrieve(self, request, pk=None):
        queryset = Anunciante.objects.all()
        anunciante = get_object_or_404(queryset, pk=pk)
        me = self.request.user.anunciante
        if anunciante != me:
            return  Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

        serializer = AnuncianteSerializer(anunciante)
        return Response(serializer.data)

    @permission_classes([AllowAny])
    def create(self, request):
        serializer = AnuncianteSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #@authentication_classes([BasicAuthentication, SessionAuthentication])
    #@permission_classes([IsAuthenticated, IsAdminUser])
    def update(self, request, pk=None):
        try:
            anunciante = Anunciante.objects.get(pk=pk)
        except Anunciante.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = AnuncianteSerializer(anunciante, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        try:
            anunciante = Anunciante.objects.get(pk=pk)
        except Anunciante.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = AnuncianteSerializer(anunciante, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #@authentication_classes([BasicAuthentication, SessionAuthentication])
    #@permission_classes([IsAuthenticated, IsAdminUser])
    def destroy(self, request, pk=None):
        try:
            anunciante = Anunciante.objects.get(pk=pk)
        except Anunciante.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        anunciante.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EnderecoViewSet(viewsets.ModelViewSet):
    serializer_class = EnderecoSerializer
    queryset = Endereco.objects.all()