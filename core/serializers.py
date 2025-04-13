from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Topic, Subscription, EmailHistory


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "password_confirmation")
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        if data.get("password") != data.get("password_confirmation"):
            raise serializers.ValidationError("Passwords don't match")
        return data

    def create(self, validated_data):
        validated_data.pop("password_confirmation")
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = "__all__"


class SubscriptionSerializer(serializers.ModelSerializer):
    topic_details = TopicSerializer(source="topic", read_only=True)

    class Meta:
        model = Subscription
        fields = ("id", "topic", "topic_details", "created_at")


class EmailHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailHistory
        fields = "__all__"
