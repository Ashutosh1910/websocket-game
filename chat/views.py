from django.shortcuts import render
from django.http import HttpResponse

import tkinter as tk

# Create your views here.

async def Home(request):
    
    
    return render(request,'chat/welcome.html')






def room(request):

    room_name=request.GET['room_name']
    player_name=request.GET['player_name']

    return render(request,'chat/room.html',context={'room_name':room_name,'player_name':player_name})