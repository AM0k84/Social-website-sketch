from django.contrib import admin

from news.models import Article, ArticleCategory, ArticleComment


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'body', 'article_categories', 'author', 'created_on', 'is_promoted', 'slug')
    prepopulated_fields = {'slug': ('title',)}


class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name', 'created_on', 'slug')
    prepopulated_fields = {'slug': ('category_name',)}


class ArticleCommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'created_on')


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleCategory, ArticleCategoryAdmin)
admin.site.register(ArticleComment, ArticleCommentAdmin)
