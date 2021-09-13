from django.conf.urls import url
from django.urls import path
from Lenders.api import LenderViewSet, UploadLenderView, DownloadLenderView
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'api/lender', LenderViewSet)
router.register(r'api/upload', UploadLenderView)
router.register(r'api/download', DownloadLenderView)
urlpatterns = router.urls
