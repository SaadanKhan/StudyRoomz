# we cannot directly pass all the model data when requested, we have to convert them into JSON Response first, that's what serializers are doing here.

from rest_framework.serializers import ModelSerializer
from app.models import Room


class RoomSerializer(ModelSerializer):
    class Meta:
        
        model = Room
        fields = '__all__'