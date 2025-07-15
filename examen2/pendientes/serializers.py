from rest_framework import serializers

class TodoSerializer(serializers.Serializer):

    userId = serializers.IntegerField()
    id = serializers.IntegerField()
    
    title = serializers.CharField(max_length=255)
    completed = serializers.BooleanField()

    def to_internal_value(self, data):
        validated_data = super().to_internal_value(data)
        
        return {
            'user_id': validated_data.get('userId'),
            'api_id': validated_data.get('id'),
            'title': validated_data.get('title'),
            'completed': validated_data.get('completed')
        }