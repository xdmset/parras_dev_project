from rest_framework import serializers

class TodoSerializer(serializers.Serializer):
    """
    Un serializador manual y explícito para validar los datos de la API.
    Este método nos da control total y evita cualquier magia de Django.
    """
    # 1. Le decimos que espere recibir un campo 'userId' y 'id' de la API.
    userId = serializers.IntegerField()
    id = serializers.IntegerField()
    
    # 2. Los otros campos se llaman igual, así que los declaramos tal cual.
    title = serializers.CharField(max_length=255)
    completed = serializers.BooleanField()

    # 3. Este método es clave. Una vez que los datos son válidos,
    #    los reestructuramos para que coincidan con nuestro modelo 'Todo'.
    def to_internal_value(self, data):
        # Llamamos primero al método padre para obtener los datos validados
        validated_data = super().to_internal_value(data)
        
        # Creamos un nuevo diccionario con los nombres de nuestro modelo
        return {
            'user_id': validated_data.get('userId'),
            'api_id': validated_data.get('id'),
            'title': validated_data.get('title'),
            'completed': validated_data.get('completed')
        }