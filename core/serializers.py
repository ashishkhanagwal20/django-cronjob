from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Topic, Subscription, EmailHistory

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'

class SubscriptionSerializer(serializers.ModelSerializer):
    topic_details = TopicSerializer(source='topic', read_only=True)

    class Meta:
        model = Subscription
        fields = ('id', 'topic', 'topic_details', 'created_at')

class EmailHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailHistory
        fields = '__all__'