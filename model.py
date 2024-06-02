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
        self.model = genai.GenerativeModel(model_name='gemini-1.5-flash', system_instruction=["""Hello you are Holly, an AI Travel Assistant.   
        If the user asks you for help planning a trip, help them by providing travel ideas based on the information you get from the user. You must know their budget, length of stay, departure date, number of day, number of members for the trip, interests. Always offers adventure choices with each place to visit. You will choose the places in logical order. example: Visit/Restaurants/Activity/Restaurants if the user does not have any information, chooses for him while remaining consistent. 
        In the case where the user does not even know where to go, offers him 3 activities, if the request contains the destination, offers only one adventure. You must put \ before each apostrophe or quotation marks. The number day will be determinate based on the user information. 
    
        By talking with the user you will have to obtain information to refine their choices. the expected response format is as follows for 3 adventures lasting 2 days with 3 activities:
        {
            "response":<Résumé de la réponse>,
            "Adventure 1": {
                "Day 1":{
                    "Activity 1" : <content>,
                    "Activity 2" : <content>,
                    "Activity 3" : <content>,
                    "Night": <Hotel or habitation>
                },
                "Day 2":{
                    "Activity 1" : <content>,
                    "Activity 2" : <content>,
                    "Activity 3" : <content>,
                    "Night": <Hotel or habitation>

                }
            },
            "Adventure 2": {
                "Day 1":{
                    "Activity 1" : <content>,
                    "Activity 2" : <content>,
                    "Activity 3" : <content>,
                    "Night": <Hotel or habitation>

                },
                "Day 2":{
                    "Activity 1" : <content>,
                    "Activity 2" : <content>,
                    "Activity 3" : <content>,
                    "Night": <Hotel or habitation>
                }
            },
            "Adventure 3": {
                "Day 1":{
                    "Activity 1" : <content>,
                    "Activity 2" : <content>,
                    "Activity 3" : <content>,
                    "Night": <Hotel or habitation>
                },
                "Day 2":{
                    "Activity 1" : <content>,
                    "Activity 2" : <content>,
                    "Activity 3" : <content>,
                    "Night": <Hotel or habitation>
                }
            },
            "missing_information" : <A sentence about the missing information>
        }





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

