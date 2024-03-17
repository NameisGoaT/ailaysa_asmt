from django.db.models import Max
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import StreamingHttpResponse
from .models import UserProfile, PostModel, UploadedFile, Category, CommentModel
from .serializers import UserProfileSerializer, PostSerializer, UploadedFileSerializer, CategorySerializer, \
    CommentModelSerializer
from .tasks import words_in_file
import time


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filters = ['name']
    filterset_fields = filters
    search_fields = filters
    ordering_fields = ['name']


class PostViewSet(viewsets.ModelViewSet):
    queryset = PostModel.objects.all()
    serializer_class = PostSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filters = ['created_at', 'title', 'author']
    filterset_fields = {'title': ['isnull'],
                        'author': ['in', 'exact'],
                        }
    search_fields = filters
    ordering_fields = ['created_at']

    def get_queryset(self):
        annotated_queryset = self.queryset.annotate(
            latest_comment_date=Max('comments__publication_date')
        )
        return annotated_queryset

    def perform_destroy(self, instance):
        instance.comments.all().delete()
        instance.delete()

    @action(detail=False, methods=['get'])
    def recent_comments(self, request):
        posts = PostModel.objects.order_by('-comments__publication_date').distinct()
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def sorted_by_created_at(self, request):
        posts = PostModel.objects.order_by('-created_at')
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'])
    def delete_if_no_comments(self, request, pk=None):
        post = self.get_object()
        if post.comments.count() == 0:
            post.delete()
            return Response({'message': 'Post deleted successfully'})
        return Response({'message': 'Post still has comments'})


def generate_sentence():
    sentences = ['This is a sentence.', 'Another sentence here.', 'One more sentence.']
    for sentence in sentences:
        time.sleep(1)
        yield f"data: {sentence}\n\n"


def stream_sentence(request):
    response = StreamingHttpResponse(generate_sentence(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    return response


class UploadedFileViewSet(viewsets.ModelViewSet):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        count_of_words = words_in_file.delay(serializer.instance.file.path)
        word_count = count_of_words.get()
        serializer.instance.word_count = word_count
        serializer_data = serializer.data

        headers = self.get_success_headers(serializer_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = CommentModel.objects.all()
    serializer_class = CommentModelSerializer


