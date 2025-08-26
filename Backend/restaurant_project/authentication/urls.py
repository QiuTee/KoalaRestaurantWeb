from django.urls import path 
from authentication.views import * 
from django.conf import settings
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register(r'manager',  ManagerAuthentications , basename = 'manager')
router.register(r'customer', CustomerAuthentications , basename='customer')


urlpatterns = [
    path('google/', GoogleSignInView.as_view(), name='google'),
]


urlpatterns += router.urls
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)