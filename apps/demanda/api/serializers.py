from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from ..models import Anunciante, Endereco, Demanda, EnderecoDeEntrega
from django.contrib.auth.models import User
from django.core import exceptions
from django.core.exceptions import ObjectDoesNotExist
import django.contrib.auth.password_validation as validators


class AdministradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username','password', 'is_superuser', 'first_name', 'last_name', 'email')

    def create(self, validated_data):
        user = User(**validated_data)
        password = validated_data.get('password')
        user.set_password(password) 
        
        user.save()
        return user

    def validate_password(self,data):
        
        try:
            validators.validate_password(password=data,user=data)

        except exceptions.ValidationError as e:
            erros = list(e.messages)
            raise serializers.ValidationError(erros)
                
        return data

class EnderecoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Endereco
        fields = ('id', 'rua', 'numero', 'bairro', 'cidade', 'estado', 'cep', 'complemento', 'anunciante')


class AnuncianteSerializer(WritableNestedModelSerializer):
    endereco_set = EnderecoSerializer(many=True, required=False, allow_null=True, default=None)    

    class Meta:
        model = Anunciante
        fields = ('id', 'username', 'password', 'email', 'is_active', 'nome', 'cpf', 'telefone', 'endereco_set')

    def create(self, validated_data):
        endereco_data = validated_data.pop('endereco_set')
        anunciante = Anunciante.objects.create(**validated_data)
        password = validated_data.get('password')
        anunciante.set_password(password)
        for endereco_data in endereco_data:
            Endereco.objects.create(anunciante=anunciante, **endereco_data) 
        
        return anunciante

    def validate_password(self,data):
        
        try:
            validators.validate_password(password=data,user=data)

        except exceptions.ValidationError as e:
            erros = list(e.messages)
            raise serializers.ValidationError(erros)
                
        return data


class EnderecoDeEntregaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = EnderecoDeEntrega
        fields = ('id', 'rua', 'numero', 'bairro', 'cidade', 'estado', 'cep', 'complemento')


class DemandaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Demanda
        fields = ('id', 'descricao', 'endereco_de_entrega', 'info_contato', 'anunciante','status')


class DemandaListaSerializer(serializers.ModelSerializer):
    endereco_de_entrega = EnderecoDeEntregaSerializer()

    class Meta:
        model = Demanda
        fields = ('id', 'descricao', 'endereco_de_entrega', 'info_contato', 'anunciante','status')
