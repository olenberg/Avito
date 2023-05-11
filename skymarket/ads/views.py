from rest_framework import pagination, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from ads.models import Ad, Comment
from ads.serializers import AdSerializer, AdDetailSerializer, CommentSerializer
from ads.permissions import IsAdmin, IsAuthor
from django_filters.rest_framework import DjangoFilterBackend
from ads.filters import AdTitleFilter


class AdPagination(pagination.PageNumberPagination):
    page_size = 4


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    pagination_class = AdPagination
    serializer_class = AdSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AdTitleFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ["retrieve", "create", "update", "partial_update", "destroy"]:
            return AdDetailSerializer
        return AdSerializer

    def get_permissions(self):
        permission_classes = (AllowAny,)
        if self.action == "retrieve":
            permission_classes = (AllowAny,)
        elif self.action in ["create", "update", "partial_update", "destroy", "me"]:
            permission_classes = (IsAuthor | IsAdmin,)
        return tuple(permission() for permission in permission_classes)

    @action(detail=False, methods=['get'])
    def me(self, request, *args, **kwargs):
        self.queryset = Ad.objects.filter(author=request.user)
        return super().list(self, request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        ad_id = self.kwargs.get("ad_pk")
        ad = get_object_or_404(Ad, id=ad_id)
        return ad.comments.all()

    def perform_create(self, serializer):
        ad_id = self.kwargs.get("ad_pk")
        ad = get_object_or_404(Ad, id=ad_id)
        user = self.request.user
        serializer.save(author=user, ad=ad)

    def get_permissions(self):
        permission_classes = (IsAuthenticated,)
        if self.action in ["list", "retrieve"]:
            permission_classes = (IsAuthenticated,)
        elif self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = (IsAuthor | IsAdmin,)
        return tuple(permission() for permission in permission_classes)
