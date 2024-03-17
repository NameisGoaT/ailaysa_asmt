from django.contrib import admin

from profiles.models import UserProfile, Category, SubCategory, PostModel, CommentModel, UploadedFile

admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(PostModel)
admin.site.register(CommentModel)
admin.site.register(UploadedFile)