from rest_framework import routers
from .views import AnuncianteViewSet, EnderecoViewSet


router = routers.DefaultRouter()

router.register('anunciante', AnuncianteViewSet, basename='anunciante')
router.register('endereco', EnderecoViewSet, basename='endereco')

urlpatterns = router.urls