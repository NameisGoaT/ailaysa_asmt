from rest_framework import serializers
from .models import UserProfile, Category, SubCategory, PostModel, CommentModel, UploadedFile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'name', 'email', 'profile_picture']


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'subcategories']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = ['id', 'comments', 'publication_date']


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    total_comments = serializers.SerializerMethodField()

    def get_total_comments(self, obj):
        return obj.comments.count()

    class Meta:
        model = PostModel
        fields = ['id', 'title', 'author', 'created_at', 'comments', 'total_comments']


class UploadedFileSerializer(serializers.ModelSerializer):
    word_count = serializers.SerializerMethodField()

    class Meta:
        model = UploadedFile
        fields = ['id', 'file', 'uploaded_at', 'word_count']

    def get_word_count(self, obj):
        if hasattr(obj, 'word_count'):
            return obj.word_count
        return None


class CommentModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentModel
        fields = "__all__"