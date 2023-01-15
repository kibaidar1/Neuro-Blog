from django.contrib import admin
from .models import Post, HotPost, User, Comment


class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email',)}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',),
        }),
    )
    list_display = ('username', 'email', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)


class PostAdmin(admin.ModelAdmin):
    fieldsets = (None, {'fields': ('title', 'url')}), \
                ('Content', {'fields': ('description', 'content', 'image')}), \
                ('Context', {'fields': ('author', 'created_at', 'tag')}),
    list_display = ('title', 'url', 'description', 'author', 'created_at',)
    list_filter = ('title', 'author', 'created_at', 'tag')
    search_fields = ('title', 'name', 'created_at', 'content', 'author',)
    prepopulated_fields = {'url': ('title',)}


class HotPostsAdmin(admin.ModelAdmin):
    # fieldsets = (None, {'fields': ('title', 'url')}), ('Author', {'fields': ('author',)}),
    # list_display = ('title', 'url', 'description', 'content', 'image', 'author', 'created_at', 'tag')
    # list_filter = ('title', 'description', 'author', 'created_at',)
    # search_fields = ('title', 'name', 'created_at', 'content', 'author', 'tag')
    # prepopulated_fields = {'url': ('title',)}
    pass


class CommentAdmin(admin.ModelAdmin):
    fields = ('post', 'author', 'created_at', 'text')
    list_display =  ('author', 'post', 'created_at')
    list_filter = ('author', 'post', 'created_at')
    search_fields = ('author', 'post')


admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(HotPost, HotPostsAdmin)
admin.site.register(Comment, CommentAdmin)
