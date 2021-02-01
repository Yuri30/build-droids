from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import  permission_classes, authentication_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.parsers import JSONParser
from rest_framework import status

from django.contrib.auth.models import User
from ..models import Anunciante, Endereco, Demanda, EnderecoDeEntrega
from .serializers import AnuncianteSerializer, EnderecoSerializer, DemandaSerializer, DemandaListaSerializer, AdministradorSerializer


class AdministradorViewSet(viewsets.ModelViewSet):
    serializer_class = AdministradorSerializer
    queryset = User.objects.filter(is_staff=True)


class AnuncianteViewSet(viewsets.ModelViewSet):
    serializer_class = AnuncianteSerializer
    queryset = Anunciante.objects.all()

    @authentication_classes([BasicAuthentication, SessionAuthentication])
    @permission_classes([IsAuthenticated, IsAdminUser])
    def list(self, request):
        queryset = Anunciante.objects.all()
        serializer = AnuncianteSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @authentication_classes([BasicAuthentication, SessionAuthentication])
    @permission_classes([IsAuthenticated])
    def retrieve(self, request, pk=None):
        queryset = Anunciante.objects.all()
        anunciante = get_object_or_404(queryset, pk=pk)
        me = self.request.user.anunciante
        if anunciante != me:
            return Response("Anunciante não é o mesmo que esta logado", status=status.HTTP_401_UNAUTHORIZED)

        serializer = AnuncianteSerializer(anunciante)
        return Response(serializer.data)

    @permission_classes([AllowAny])
    def create(self, request):
        serializer = AnuncianteSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @authentication_classes([BasicAuthentication, SessionAuthentication])
    @permission_classes([IsAuthenticated,])
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
    
    @authentication_classes([BasicAuthentication, SessionAuthentication])
    @permission_classes([IsAuthenticated,])
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

    @authentication_classes([BasicAuthentication, SessionAuthentication])
    @permission_classes([IsAuthenticated, IsAdminUser])
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
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        me = self.request.user.anunciante
        queryset = Endereco.objects.filter(anunciante=me)
        serializer = EnderecoSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Anunciante.objects.all()
        anunciante = get_object_or_404(queryset, pk=pk)
        me = self.request.user.anunciante
        if anunciante != me:
            return Response("Endereço não é do Anunciante que esta logado", status=status.HTTP_401_UNAUTHORIZED)

        serializer = AnuncianteSerializer(anunciante)
        return Response(serializer.data)

    def create(self, request):
        serializer = EnderecoSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DemandaViewSet(viewsets.ModelViewSet):
    serializer_class = DemandaSerializer
    queryset = Demanda.objects.all()

    @parser_classes([JSONParser])
    @permission_classes([IsAuthenticated])
    def create(self, request, format=None):
        print(request.data['anunciante'])
        anunciante = Anunciante.objects.get(id=request.data['anunciante'])
        info = {'nome': anunciante.nome, 'email': anunciante.email, 'telefone': anunciante.telefone}
        endereco = Endereco.objects.get(id=request.data['endereco_de_entrega'])
        endereco_de_entrega = EnderecoDeEntrega.objects.create(rua=endereco.rua, numero=endereco.numero, bairro=endereco.bairro, cidade=endereco.cidade, cep=endereco.cep, complemento=endereco.complemento)
        serializer = DemandaSerializer(data={'descricao': request.data['descricao'], 'endereco_de_entrega': endereco_de_entrega.id, 'info_contato': info, 'anunciante': request.data['anunciante'],'status': request.data['status']})

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @authentication_classes([BasicAuthentication, SessionAuthentication])
    @permission_classes([IsAuthenticated,])
    def list(self, request):
        me = self.request.user.anunciante
        queryset = Demanda.objects.filter(anunciante=me)
        serializer = DemandaListaSerializer(queryset, many=True)
        return Response(serializer.data)

    @authentication_classes([BasicAuthentication, SessionAuthentication])
    @permission_classes([IsAuthenticated,])
    def update(self, request, pk=None):
        try:
            demanda = Demanda.objects.get(pk=pk)
            me = self.request.user.anunciante
            if demanda.anunciante != me:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except Demanda.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = DemandaSerializer(demanda, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @authentication_classes([BasicAuthentication, SessionAuthentication])
    @permission_classes([IsAuthenticated,])
    def partial_update(self, request, pk=None):
        try:
            demanda = Demanda.objects.get(pk=pk)
            me = self.request.user.anunciante
            if demanda.anunciante != me:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except Demanda.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = DemandaSerializer(demanda, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @authentication_classes([BasicAuthentication, SessionAuthentication])
    @permission_classes([IsAuthenticated,])
    def destroy(self, request, pk=None):
        try:
            demanda = Demanda.objects.get(pk=pk)
            me = self.request.user.anunciante
            if demanda.anunciante != me:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except Demanda.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        demanda.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)