from flask import Flask, json, request, jsonify
from model import ChatBot
from utils import *
from flask_cors import CORS, cross_origin


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
    return response._result.candidates[0].content.parts[0].text

@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        if file.filename.lower().endswith('.pdf'):
            pdf_text = extract_text_from_pdf(file)
            return jsonify({"pdf_text": pdf_text}), 200
        elif file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_text = extract_text_from_image(file)
            return jsonify({"image_text": image_text}), 200

    return jsonify({"error": "Invalid file type"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)