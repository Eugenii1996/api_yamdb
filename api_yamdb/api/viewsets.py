from rest_framework import mixins
from rest_framework import viewsets


class CreateGetDeleteViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                       mixins.DestroyModelMixin, viewsets.GenericViewSet):
    pass
