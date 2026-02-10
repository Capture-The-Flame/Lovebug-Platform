from django.contrib import admin
from .models import Challenge, UserChallenge

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category',
        'base_points', 'solves_count', 'current_points_display',
        'is_active', 'created_at'
    ]
    list_filter = ['category', 'is_active']
    search_fields = ['title', 'description']
    ordering = ['-created_at'] 

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'category')
        }),
        ('Scoring', {
            'fields': ('base_points', 'decrement', 'min_points', 'solves_count')
        }),
        ('Challenge Content', {
            'fields': ('description', 'prompt', 'flag')
        }),
        ('Hints', {
            'fields': ('hint_1', 'hint_2', 'hint_3'),
            'classes': ('collapse',)
        }),
        ('Settings', {
            'fields': ('is_active',)
        }),
    )

    @admin.display(description="Points (current)")
    def current_points_display(self, obj):
        return obj.current_points


@admin.register(UserChallenge)
class UserChallengeAdmin(admin.ModelAdmin):
    list_display = ['user', 'challenge', 'awarded_points', 'completed_at']
    list_filter = ['completed_at', 'challenge__category']
    search_fields = ['user__username', 'user__email', 'challenge__title']
    ordering = ['-completed_at']
    readonly_fields = ['completed_at']
