from flask import Flask, request, jsonify
from model import ChatBot
from flask_cors import CORS, cross_origin
import google.generativeai as genai
import os
app = Flask(__name__)
CORS(app) 


chatbot = ChatBot()
chatbot.initConv()

@app.route('/map', methods=['GET'])
@cross_origin()
def map():
    msg = ""
    for i in range(len(chatbot.chat.history)):
        msg += chatbot.chat.history[i].parts[0].text + " "

    response = chatbot.get_json(
        msg
    )
    return response

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    response = chatbot.send_message(data['content'])
    print(response._result.candidates[0].content.parts)
    return response._result.candidates[0].content.parts[0].text

@app.route('/upload_file', methods=['POST'])
def upload_file():
  current_directory = os.getcwd()
  direcory = os.path.join(current_directory , "test2.png")
  sample_file = genai.upload_file(path = direcory , display_name ="voyage" )
  print(sample_file)
  response = chatbot.model.generate_content(["describe the image" , sample_file])
  chatbot.chat.history.append({
    "role":"user" ,
    "parts":[{"text":response.text}]})
  return (response.text)
  

@app.route('/summarize', methods=['GET']) 
def summarize():

  msg = ""
  for i in range(len(chatbot.chat.history)):
    msg += chatbot.chat.history[i].parts[0].text + " "

  response = chatbot.get_json(
      msg
    )
  map_response = response
  
  summary_response = chatbot.send_message(f"Please summarize JSON the following itinerary: {map_response}") 
 
  summary_text = summary_response._result.candidates[0].content.parts[0].text
  summarized_response = { "summary": summary_text, "details": map_response } 
  return jsonify(summarized_response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)