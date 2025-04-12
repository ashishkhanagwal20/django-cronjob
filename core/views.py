from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Topic, Subscription, EmailHistory
from .serializers import TopicSerializer, SubscriptionSerializer, EmailHistorySerializer

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class SubscriptionViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        queryset = Subscription.objects.filter(user=request.user)
        serializer = SubscriptionSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        topic = get_object_or_404(Topic, id=request.data.get('topic'))
        subscription = Subscription.objects.create(
            user=request.user,
            topic=topic
        )
        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        subscription = get_object_or_404(Subscription, id=pk, user=request.user)
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class EmailHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EmailHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return EmailHistory.objects.filter(user=self.request.user)