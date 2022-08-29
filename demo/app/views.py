from django.contrib.auth.models import Group, User
from django_celery_results.models import TaskResult
from django.http import FileResponse
from rest_framework import permissions,  viewsets, decorators

from demo.app import serializers, models


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class TaskResultViewSet(viewsets.ModelViewSet):
    queryset = TaskResult.objects.all()
    serializer_class = serializers.TaskResultSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'task_id'


class MyModelViewSet(viewsets.ModelViewSet):
    queryset = models.MyModel.objects.all()
    serializer_class = serializers.MyModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    @decorators.action(methods=['post'], detail=True)
    def download(self, request, pk=None, *args, **kwargs):
        file_obj = self.get_object()
        response = FileResponse(
            open(file_obj.upload.path, 'rb'), as_attachment=True)
        return response
