from home.models import Task, CustomUser
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email']


class TaskSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
        # fields = ['title', 'description']

    
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        task = Task.objects.create(**validated_data)
        return task


class UpdateTaskSerializer(serializers.Serializer):
    is_deleted = serializers.BooleanField(required=False, default=None)
    is_done = serializers.BooleanField(required=False, default=None)


    def update(self,instance, validated_data):
        is_deleted = validated_data.get('is_deleted', None)
        is_done = validated_data.get('is_done', None)
        
        if is_deleted:
            instance.is_deleted = is_deleted
        if is_done:
            instance.is_done = is_done
        
        instance.save()

        return instance