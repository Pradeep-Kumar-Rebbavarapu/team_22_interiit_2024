import json
from channels.generic.websocket import WebsocketConsumer
# Import the LLM function
from .agent import agentAI  # Assuming the LLM code is in llm.py in the same directory

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        try:
            # Parse incoming message
            data = json.loads(text_data)
            message = data.get("message", "")

            # Send message to LLM and get response
            llm_response = agentAI(message)
            print(llm_response)
            # Send response back to client
            self.send(text_data=json.dumps({
                'status': 'success',
                'message': str(llm_response)
            }))

        except Exception as e:
            # Handle any errors and send error message to client
            self.send(text_data=json.dumps({
                'status': 'error',
                'message': f'Error processing message: {str(e)}'
            }))