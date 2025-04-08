from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Question, Answer

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_link', 'created_at', 'answer_count', 'is_recent')
    list_filter = ('created_at', 'author', 'updated_at')
    search_fields = ('title', 'content', 'author__username')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'author')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def author_link(self, obj):
        url = reverse('admin:auth_user_change', args=[obj.author.id])
        return format_html('<a href="{}">{}</a>', url, obj.author.username)
    author_link.short_description = 'Author'
    
    def answer_count(self, obj):
        count = obj.answers.count()
        url = reverse('admin:qa_answer_changelist') + f'?question__id__exact={obj.id}'
        return format_html('<a href="{}">{} answers</a>', url, count)
    answer_count.short_description = 'Answers'
    
    def is_recent(self, obj):
        from django.utils import timezone
        from datetime import timedelta
        if obj.created_at >= timezone.now() - timedelta(days=7):
            return format_html('<span style="color: green;">✓</span>')
        return format_html('<span style="color: gray;">-</span>')
    is_recent.short_description = 'Recent'
    
    def mark_as_featured(self, request, queryset):
        queryset.update(featured=True)
    mark_as_featured.short_description = "Mark selected questions as featured"
    
    actions = ['mark_as_featured']

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question_link', 'author_link', 'created_at', 'like_count', 'is_recent')
    list_filter = ('created_at', 'author', 'updated_at')
    search_fields = ('content', 'author__username', 'question__title')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('question', 'content', 'author')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Likes', {
            'fields': ('likes',),
            'classes': ('collapse',)
        }),
    )
    
    def question_link(self, obj):
        url = reverse('admin:qa_question_change', args=[obj.question.id])
        return format_html('<a href="{}">{}</a>', url, obj.question.title)
    question_link.short_description = 'Question'
    
    def author_link(self, obj):
        url = reverse('admin:auth_user_change', args=[obj.author.id])
        return format_html('<a href="{}">{}</a>', url, obj.author.username)
    author_link.short_description = 'Author'
    
    def like_count(self, obj):
        return obj.likes.count()
    like_count.short_description = 'Likes'
    
    def is_recent(self, obj):
        from django.utils import timezone
        from datetime import timedelta
        if obj.created_at >= timezone.now() - timedelta(days=7):
            return format_html('<span style="color: green;">✓</span>')
        return format_html('<span style="color: gray;">-</span>')
    is_recent.short_description = 'Recent'
    
    def mark_as_featured(self, request, queryset):
        queryset.update(featured=True)
    mark_as_featured.short_description = "Mark selected answers as featured"
    
    actions = ['mark_as_featured']
