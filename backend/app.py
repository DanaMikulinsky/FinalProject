from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

from pipeline.Chatbot import Chatbot, DBHandler

from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

db_handler = None
chatbot = None

# Initialize the Chatbot
@app.route('/api/create_chatbot', methods=['POST'])
def create_chatbot():
    global db_handler, chatbot

    if request.method != 'POST':
        return jsonify({'error': 'Only POST requests are allowed'})
    else:
        data = request.get_json()
        if data:
            print(data)
            org_id = data.get('org_id')
            user_id = data.get('user_id')
            style = data.get('style')
            db_handler = DBHandler(org_id, user_id)
            chatbot = Chatbot(db_handler, style)

            to_return = {
                'message': 'Chatbot created',
                'org_id': org_id,
                'user_id': user_id,
                'chat': chatbot.__repr__(),
                'db': db_handler.__repr__()
            }
            return jsonify(to_return)
        else:
            return jsonify({'error': 'No data provided'})


# Get the chat history
@app.route('/api/get_history', methods=['GET'])
def get_history():
    global db_handler

    if request.method != 'GET':
        return jsonify({'error': 'Only GET requests are allowed'})
    else:
        if not db_handler:
            return jsonify({'error': 'Chatbot not created yet'})
        else:
            history = db_handler.get_history()
            return jsonify({'history': history})


# Run the RAG pipeline
@app.route('/api/answer_question', methods=['POST'])
def answer_question():
    global chatbot

    if request.method != 'POST':
        return jsonify({'error': 'Only POST requests are allowed'})
    else:
        if not chatbot:
            return jsonify({'error': 'Chatbot not created yet'})
        else:
            data = request.get_json()
            if data:
                question = data.get('question')
                answer = chatbot.answer_question(question)
                return jsonify({'answer': answer})
            else:
                return jsonify({'error': 'No data provided'})


# Reset the chat history
@app.route('/api/reset_history', methods=['DELETE'])
def reset_history():
    global db_handler

    if request.method != 'DELETE':
        return jsonify({'error': 'Only DELETE requests are allowed'})
    else:
        if not db_handler:
            return jsonify({'error': 'Chatbot not created yet'})
        else:
            db_handler.reset_history()
            return jsonify({'message': 'Chat history reset'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

