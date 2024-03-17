from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserProfileViewSet, PostViewSet, stream_sentence, UploadedFileViewSet, CategoryViewSet, \
    CommentViewSet

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet)
router.register(r'posts', PostViewSet)
router.register(r'files', UploadedFileViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('stream-sentence/', stream_sentence),
]
