#-------------------Sample For every Project
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        # To access all rooms
        'GET /api/room',

        # To access specific room by id
        'GET /api/room/:id'
    ]

    return Response(routes)
#-------------------Sample For every Project

from app.models import Room
from .serializers import RoomSerializer

# Through this decorator we specify that this function is for API
@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getRoom(request, pk):
    room = Room.objects.get(id = pk)
    serializer = RoomSerializer(room,many=False)
    return Response(serializer.data)