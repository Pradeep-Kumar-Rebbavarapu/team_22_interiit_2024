import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import MatchInfo
from .agent import agentAI
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    @database_sync_to_async
    def get_match_players(self, match_id):
        try:
            match = MatchInfo.objects.get(id=match_id)
            team_a_players = list(match.team_a_players.values_list('name', flat=True))
            team_b_players = list(match.team_b_players.values_list('name', flat=True))
            return team_a_players + team_b_players
        except MatchInfo.DoesNotExist:
            return []

    async def receive(self, text_data):
        try:
            # Parse incoming message
            data = json.loads(text_data)
            message = data.get("message", "")
            match_id = data.get("match_id", "")

            # Get players asynchronously
            all_players = await self.get_match_players(match_id)

            # Send message to LLM and get response
            llm_response = await self.run_agent_ai(message, all_players)

            # Send response back to client
            await self.send(text_data=json.dumps({
                'status': 'success',
                'message': str(llm_response)
            }))

        except Exception as e:
            await self.send(text_data=json.dumps({
                'status': 'error',
                'message': f'Error processing message: {str(e)}'
            }))

    @database_sync_to_async
    def run_agent_ai(self, message, all_players):
        # Wrap the synchronous agentAI function 
        return agentAI(message, all_players)