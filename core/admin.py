from django.contrib import admin
from .models import Topic, Subscription, EmailHistory


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("title", "search_query", "created_at")
    search_fields = ("title", "description", "search_query")
    list_filter = ("created_at",)
    ordering = ("-created_at",)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "topic")
    list_filter = ("topic",)
    search_fields = ("user__username", "topic__title")


@admin.register(EmailHistory)
class EmailHistoryAdmin(admin.ModelAdmin):
    list_display = ("user", "subject", "sent_at")
    list_filter = ("sent_at",)
    search_fields = ("user__username", "subject", "content")
    ordering = ("-sent_at",)
