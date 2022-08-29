from django.contrib.auth.models import Group, User
from django_celery_results.models import TaskResult
from rest_framework import serializers

from demo.app.models import MyModel


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class TaskResultSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='taskresult-detail',
        lookup_field='task_id'
    )

    class Meta:
        model = TaskResult
        fields = '__all__'


class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'
