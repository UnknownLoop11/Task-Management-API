from rest_framework import serializers
from main.models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        # Exclude the user field from the input validation
        extra_kwargs = {
            'user': {'required': False, 'allow_null': True}
        }

    def update(self, instance, validated_data):
        previous_status = instance.status

        # Update fields only if they are provided in validated_data
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.due_date = validated_data.get('due_date', instance.due_date)

        # Validate status transitions if the status is provided
        new_status = validated_data.get('status', instance.status)
        if new_status != previous_status:
            if (previous_status == 'pending' and new_status == 'in_progress') or \
               (previous_status == 'in_progress' and new_status == 'completed'):
                instance.status = new_status
            else:
                raise serializers.ValidationError('Invalid status transition')

        instance.save()
        return instance
