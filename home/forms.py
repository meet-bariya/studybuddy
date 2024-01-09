from django.forms import ModelForm
from .models import Room, User

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ['name','topic','description']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['name','username','email','bio']