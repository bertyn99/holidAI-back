# import pathlib
# import textwrap

# import google.generativeai as genai

# from IPython.display import display
# from IPython.display import Markdown

# # Used to securely store your API key
# from google.colab import userdata

# # Or use `os.getenv('GOOGLE_API_KEY')` to fetch an environment variable.
# GOOGLE_API_KEY=userdata.get('GOOGLE_API_KEY')

# genai.configure(api_key=GOOGLE_API_KEY)

# model = genai.GenerativeModel('gemini-1.5-flash')

# chat = model.start_chat(history=[])
# response = chat.send_message("In one sentence, explain how a computer works to a young child.")

import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()


class ChatBot:
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_API_KEY')
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.chat = None
        self.configure()

    def configure(self):
        genai.configure(api_key=self.api_key)
    
    def initConv(self):
        self.chat = self.model.start_chat(history=[])
    
    def send_message(self, message):
        if not self.chat:
            raise Exception("Chat model is not initialized.")
        response = self.chat.send_message(message)
        return response

# Usage example:
# GOOGLE_API_KEY = 'your-api-key-here'
# chatbot = ChatBot(GOOGLE_API_KEY)
# response = chatbot.send_message("In one sentence, explain how a computer works to a young child.")
# print(response)
