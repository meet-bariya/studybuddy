from rest_framework.decorators import api_view
from rest_framework.response import Response
from home.models import Room, Topic
from .serializers import RoomSerializer, TopicSerializer

@api_view(['GET'])
def get_routes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id',
        'GET /api/topics'
    ]
    res = {'routes':routes}
    return Response(res)

@api_view(['GET'])
def get_rooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    res = {'rooms':serializer.data}
    return Response(res)

@api_view(['GET'])
def get_room(request,pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False)
    res = {'room':serializer.data}
    return Response(res)

@api_view(['GET'])
def get_topics(request):
    data = Topic.objects.all()
    topics = TopicSerializer(data, many=True)
    res = {'topics':topics.data}
    return Response(res)