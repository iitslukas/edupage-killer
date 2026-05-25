from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Channel, ChannelMembership, Message
from .serializers import ChannelSerializer, MessageSerializer


class ChannelListView(generics.ListCreateAPIView):
    serializer_class = ChannelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):  # type: ignore[override]
        return Channel.objects.filter(members=self.request.user, is_archived=False)

    def perform_create(self, serializer):  # type: ignore[override]
        channel = serializer.save(created_by=self.request.user)
        ChannelMembership.objects.create(channel=channel, user=self.request.user, is_admin=True)


class ChannelDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ChannelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):  # type: ignore[override]
        return Channel.objects.filter(members=self.request.user)


class MessageListView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):  # type: ignore[override]
        channel_id = self.kwargs["channel_id"]
        return Message.objects.filter(
            channel_id=channel_id,
            channel__members=self.request.user,
            is_deleted=False,
        ).select_related("author").order_by("created_at")

    def perform_create(self, serializer):  # type: ignore[override]
        serializer.save(author=self.request.user, channel_id=self.kwargs["channel_id"])


class JoinChannelView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, channel_id):  # type: ignore[override]
        channel = Channel.objects.get(pk=channel_id)
        ChannelMembership.objects.get_or_create(channel=channel, user=request.user)
        return Response({"joined": True}, status=status.HTTP_200_OK)
