from .serializers import AnuncianteSerializer


__all__ = ['jwt_response_payload_handler']


def jwt_response_payload_handler(token, user=None, request=None):
    
    if hasattr(user, 'anunciante'):
        user = AnuncianteSerializer(user.anunciante, context={'request': request}).data
        del user['password']
        return {
        'token': token,
        'artista': user,
    }