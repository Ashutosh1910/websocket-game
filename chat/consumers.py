from channels.generic.websocket import AsyncWebsocketConsumer

import json
import random
import secrets


class Message:

    ERROR_TYPES=['CONNECTION-LIMIT','OUT-OF-TURN','INVALID-INPUT']
    def __init__(self,player_name,room_name,):
        self.player_name=player_name
        self.room_name=room_name

    def error(self,error_type,**kwargs):
        err_msg={'error':error_type,'kwargs':kwargs}
        return json.dumps(err_msg)

        

    def normal(self,message,sender=None,**kwargs):
        final_message={'message':message,'kwargs':kwargs,'sender':sender}
        if not final_message['sender']:
            final_message['sender']=self.player_name

        return json.dumps(final_message)
    
    def group_message(self,type,message):
        grp_msg={'type':type,'message':message,'sender':self.player_name}

        return grp_msg
    
    def server_msg(self,type,message):
        grp_msg={'type':type,'message':message,'sender':'Server'}
        return grp_msg
    

    


        





        
    
class GameData:
    def __init__(self) -> None:
        pass


class RussianRouletteGame(AsyncWebsocketConsumer):

    ongoing_games={}
    async def connect(self):
        
        q=self.scope['query_string'].decode('utf-8')
    
        self.room_name=(q.split("&")[0].split('=')[1])
        self.player_name=q.split('&')[1].split('=')[1]
        await self.channel_layer.group_add(self.room_name,self.channel_name)
        await self.accept()
        self.message_obj=Message(self.player_name,self.room_name)
        await self.send(text_data=self.message_obj.normal('Welcome to Russian Roulette'))

        

        try:



            if RussianRouletteGame.ongoing_games[self.room_name].get('player2',None):
                await self.send(self.message_obj.error('lobby full'))
                
                return
            game=RussianRouletteGame.ongoing_games[self.room_name]
            RussianRouletteGame.ongoing_games[self.room_name]['player2']={'name':self.player_name}
            RussianRouletteGame.ongoing_games[self.room_name]["last_played"]=self.player_name
            starter=RussianRouletteGame.ongoing_games[self.room_name]['player1']['name']
            await self.channel_layer.group_send(self.room_name,self.message_obj.server_msg('server_send',f'Game will now start by {starter}'))
            print(RussianRouletteGame.ongoing_games[self.room_name]['num'])

        except KeyError:
            RussianRouletteGame.ongoing_games[self.room_name]={'player1':{"name":self.player_name},'num':random.randint(1,7)}
            await self.send(text_data=self.message_obj.normal(message='Waiting for player 2...'))


    async def disconnect(self, code):

        try:

            del RussianRouletteGame.ongoing_games[self.room_name]
        except KeyError:
            pass

       

        await self.channel_layer.group_discard(self.room_name,self.channel_name)
        await self.channel_layer.group_send(self.room_name,self.message_obj.server_msg('server_send','Game lost due to network issues,Please refresh'))

        await self.close()

    async def receive(self, text_data=None, bytes_data=None):

        try:
            game=RussianRouletteGame.ongoing_games[self.room_name]['player2']
        except KeyError:
            await self.send(self.message_obj.error(error_type='Still waiting for player 2'))



        mesaage=json.loads(text_data)
        if RussianRouletteGame.ongoing_games[self.room_name]['last_played']==self.player_name:
            await self.send(self.message_obj.error('out of turn'))
            print('error')
            return
        

        

        try:
            num=int(mesaage['message'])
        except ValueError:
            await self.send(self.message_obj.error('invalid input'))
            print('invalid input')
            return
        
        RussianRouletteGame.ongoing_games[self.room_name]['last_played']=self.player_name

        await self.channel_layer.group_send(self.room_name,self.message_obj.server_msg('server_send',mesaage['message']))

        if num==RussianRouletteGame.ongoing_games[self.room_name]['num']:
            await self.channel_layer.group_send(self.room_name,self.message_obj.server_msg('server_send',f'{self.player_name} died'))
            
        else:
            await self.channel_layer.group_send(self.room_name,self.message_obj.server_msg('server_send',f'{self.player_name} survived'))
            await self.channel_layer.group_send(self.room_name,self.message_obj.server_msg('server_send',f'Next player plays'))









        

    async def server_send(self,event):

        message=event['message']

        await self.send(self.message_obj.normal(message=message))
        


    async def game_message(self,event):
        pass


    
        

        


        

        





       
        






