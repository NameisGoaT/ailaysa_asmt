from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver


class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)


class Category(models.Model):
    name = models.CharField(max_length=100)


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)


class PostModel(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


class CommentModel(models.Model):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='comments')
    comments = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)


@receiver(post_delete, sender=CommentModel)
def delete_post_if_no_comments(sender, instance, **kwargs):
    post = instance.post
    if post.comments.count() == 0:
        post.delete()


class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploaded_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
