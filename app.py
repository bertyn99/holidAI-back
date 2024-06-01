from flask import Flask, request, jsonify
from model import ChatBot

app = Flask(__name__)

chatbot = ChatBot()
chatbot.initConv()

@app.route('/map', methods=['POST'])
def map():
    return jsonify("{msg: hello world map}")

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    response = chatbot.send_message(data['content'])
    print(response._result.candidates[0].content.parts)
    return response._result.candidates[0].content.parts[0].text

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)