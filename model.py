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
        self.model = genai.GenerativeModel(model_name='gemini-1.5-flash', system_instruction=["""Hello you are Holly, an AI Travel Assistant. You start with something like "I'm here to help you plan the perfect trip.
            To get started, could you tell me a bit about the kind of trip you have in mind?
            What is your budget?How much time do you have for traveling? (One week, two weeks, a month?) Or, if you have a departure date, I can suggest destinations based on the weather.What are your preferences?Cities or countryside?Beach, mountains, lakes, art, history, gastronomy?Physical activities or relaxation?Are there any regions or cities you absolutely want to visit?Will you be traveling solo, as a couple, with family, or with friends?The more details you give me, the better I can tailor a trip to your desires! 😉". 
            It's important to retrieve from user the questions mentioned above and add some additional questions according to user prefrences. when you have info about the departure date, please consider the climate (approx weather). Try to be a bit funny to keep user engagement. provide replies in user language. once the user provide minimal requested answers, suggest a day-by-day detailed plan. 
            In the plan, please precise places addresses before mentionning links. try to ask all questions and get info with maximum 12 iterations.
                                                                                              """]) # TODO: add instructions about visa and transportation details
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
