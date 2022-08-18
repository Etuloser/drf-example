from demo.app.tasks import add
from django.contrib.auth.models import Group, User
from django_celery_results.models import TaskResult
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.reverse import reverse_lazy
from rest_framework.views import APIView

from .serializers import (GroupSerializer, MyRespSerializer,
                          TaskResultSerializer, UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class TaskResultViewSet(viewsets.ModelViewSet):
    queryset = TaskResult.objects.all()
    serializer_class = TaskResultSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'task_id'


class AddTask(APIView):
    """
    View to delay add task.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        """
        Return add task id
        """
        result = add.apply_async((2, 2), countdown=5)
        serializer = MyRespSerializer(data={
            'data': [
                {
                    'task_id': result.task_id,
                    'url': f"{reverse_lazy('api-root', request=request)}tasks/{result.task_id}/"
                }
            ],
            'ret_code': 200,
            'ret_info': result.status,
        })
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response({
                'data': '',
                'ret_code': 500,
                'ret_info': serializer.errors
            })