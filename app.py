from flask import Flask, request, jsonify
from model import ChatBot
from flask_cors import CORS, cross_origin
import fitz  # PyMuPDF

app = Flask(__name__)
CORS(app)

chatbot = ChatBot()
chatbot.initConv()

@app.route('/map', methods=['GET'])
@cross_origin()
def map():
    print(chatbot.chat.history)
    response = chatbot.send_message("""L'output doit etre sous format, Envoi moi les informations que l'utilisateur t'a donnee dans un format json brut et valide comme ici avec en plus les lieux d'interet que tu lui propose: {...}""")
    return response._result.candidates[0].content.parts[0].text

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    pdf_text = data.get('pdf_text', "")
    content = data['content']
    

    print(response._result.candidates[0].content.parts)
    return response._result.candidates[0].content.parts[0].text

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        pdf_text = extract_text_from_pdf(file)
        return jsonify({"pdf_text": pdf_text}), 200

    return jsonify({"error": "Invalid file type"}), 400

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf'}

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
