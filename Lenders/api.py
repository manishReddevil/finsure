import csv, os, secrets
from django.conf import settings
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework import mixins, status, serializers
from rest_framework.response import Response

from Lenders.models import Lenders
from .serializers import LendersSerializer, FileUploadSerializer


class LenderViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin,
                                mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                                mixins.DestroyModelMixin):
    """
    A simple ViewSet for viewing and editing lenders.
    """
    queryset = Lenders.objects.all()
    serializer_class = LendersSerializer
    permission_classes = [AllowAny]


class UploadLenderView(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """
    ViewSet for uploading.
    """
    queryset = Lenders.objects.all()
    serializer_class = FileUploadSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except Exception as e:
            raise serializers.ValidationError({'detail': str(e)})
        return Response({"status": "success"},
                        status.HTTP_201_CREATED)


class DownloadLenderView(viewsets.GenericViewSet, mixins.ListModelMixin):
    """
    ViewSet for downloading the csv file.
    """
    queryset = Lenders.objects.all()
    serializer_class = LendersSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset().values('name', 'code', 'upfront_commission_rate', 'trial_commission_rate', 'active')
        filename = "{}.csv".format(secrets.token_hex(3)) # filename is randomized with unique hex
        path = os.path.join(os.path.dirname(settings.BASE_DIR), 'csvstorage') # path for the folder the csv file will be saved
        if not os.path.exists(path): # makes a directory if there is no folder
            os.mkdir(path)

        filepath = os.path.join(path, filename)
        # column_mapper created as in serializers.py
        column_mapper = {
            'name': 'Name',
            'code': 'Code',
            'upfront_commission_rate': 'Upfront Commission Rate',
            'trial_commission_rate': 'Trial Commission Rate',
            'active': 'Active Status'
        }
        valid_column = ['Name', 'Code', 'Upfront Commission Rate', 'Trial Commission Rate', 'Active Status']

        with open(filepath, 'w') as fpath:
            writer = csv.DictWriter(fpath, fieldnames=valid_column)
            writer.writeheader() # writing the headers based on the valid_column provided
            for data in qs:
                lender = dict()
                for k, v in data.items():
                    lender[column_mapper.get(k)] = v # writing the key and value from data and appending the dict
                writer.writerow(lender)

        response = HttpResponse(filepath, content_type="text/csv") # sending response sating the file is saved as a file type
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename) # force saving file

        return response
