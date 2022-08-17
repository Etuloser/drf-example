from demo.app.tasks import add
from django.contrib.auth.models import Group, User
from django.http import JsonResponse
from rest_framework import permissions, viewsets

from .serializers import GroupSerializer, UserSerializer


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


def index(request):
    return JsonResponse({
        'code': 200,
        'msg': 'success'
    })


def add_delay(request):
    res = add.delay(10, 10)
    return JsonResponse({
        'code': 200,
        'msg': 'success'
    })
