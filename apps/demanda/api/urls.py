from rest_framework import routers
from .views import AnuncianteViewSet, EnderecoViewSet, DemandaViewSet, AdministradorViewSet


router = routers.DefaultRouter()

router.register('administrador', AdministradorViewSet, basename='administrador')
router.register('anunciante', AnuncianteViewSet, basename='anunciante')
router.register('endereco', EnderecoViewSet, basename='endereco')
router.register('demanda', DemandaViewSet, basename='demanda')

urlpatterns = router.urls