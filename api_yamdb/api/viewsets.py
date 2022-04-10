from rest_framework import mixins, viewsets


class CreateGetDeleteViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                       mixins.DestroyModelMixin, viewsets.GenericViewSet):
    pass
