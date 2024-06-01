import google.generativeai as genai
import google.ai.generativelanguage as glm
from vertexai.generative_models import (Tool)
import textwrap
import json

import os
from dotenv import load_dotenv

load_dotenv()

add_to_database = glm.FunctionDeclaration(
    name="add_to_database",
    description=textwrap.dedent("""\
        Adds entities to the database.
        """),
    parameters=glm.Schema(
            type = glm.Type.OBJECT,
            properties = {
                'trip':  glm.Schema(type=glm.Type.OBJECT,
                    properties = {
                        'start_date': glm.Schema(type=glm.Type.STRING),
                        'duration': glm.Schema(type=glm.Type.STRING),
                        'budget_per_person': glm.Schema(type=glm.Type.STRING),
                        'interests': glm.Schema(type=glm.Type.STRING),
                        'travelers': glm.Schema(type=glm.Type.INTEGER),
                        }
                    ),
                'itinerary': glm.Schema(type=glm.Type.ARRAY,
                                        items = glm.Schema(type = glm.Type.OBJECT,
                                                           properties = {
                                            'day': glm.Schema(type=glm.Type.STRING),
                                            'destinations': glm.Schema(type=glm.Type.ARRAY,
                                                                       items = glm.Schema(type=glm.Type.OBJECT,
                                                                                        properties =  {
                                                                           'name': glm.Schema(type=glm.Type.STRING),
                                                                           'address': glm.Schema(type=glm.Type.STRING),
                                                                        #    'coordinates': glm.Schema(type=glm.Type.STRING),
                                                                           'transport': glm.Schema(type=glm.Type.STRING),
                                                                           'price': glm.Schema(type=glm.Type.STRING),
                                                                        #    'ticket_link': glm.Schema(type=glm.Type.STRING),
                                                                           'weather': glm.Schema(type=glm.Type.STRING),
                                                                       }))
                                        })
                )
            },
            required=['trip', 'start_date', 'duration', 'budget_per_person', 'interests', 'travelers', 'itinerary', 'day', 'destinations', 'name', 'address', 'transport', 'price', 'weather']
        )
)

model = model = genai.GenerativeModel(
    model_name='models/gemini-1.5-pro-latest',
    tools=[add_to_database])

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
    

    
    def get_json(self, message):

        result = model.generate_content(f"""
Please add the people, places, things, and relationships from this story to the database:

{message}
""",
    # Force a function call
    tool_config={'function_calling_config': 'ANY'})

        fc = result.candidates[0].content.parts[0].function_call

        return json.dumps(type(fc).to_dict(fc)['args'], indent=4)

