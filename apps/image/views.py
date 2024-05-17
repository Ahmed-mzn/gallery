from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Image
from .serializers import ImageSerializer
from .permissions import IsBetaPlayer


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsBetaPlayer]
        return super(ImageViewSet, self).get_permissions()

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)
