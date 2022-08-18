from django.contrib.auth.models import Group, User
from django_celery_results.models import TaskResult
from rest_framework import serializers


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


class MyResp:
    def __init__(self, data, ret_code, ret_info):
        self.data = data
        self.ret_code = ret_code
        self.ret_info = ret_info


class DataSerializer(serializers.Serializer):
    task_id = serializers.CharField()
    url = serializers.URLField()


class MyRespSerializer(serializers.Serializer):
    data = DataSerializer(required=False, many=True)
    ret_code = serializers.IntegerField()
    ret_info = serializers.CharField()

    def create(self, validated_data):
        return MyResp(**validated_data)

    def update(self, instance, validated_data):
        instance.data = validated_data.get('data', instance.data)
        instance.ret_code = validated_data.get('ret_code', instance.ret_code)
        instance.ret_info = validated_data.get('ret_info', instance.ret_info)
        return instance
