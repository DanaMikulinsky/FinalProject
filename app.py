from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

from dotenv import load_dotenv

from pipeline.Chatbot import Chatbot, DBHandler

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
            user_id = data.get('user_id')
            db_handler = DBHandler(user_id)
            chatbot = Chatbot(db_handler)

            to_return = {
                'message': 'Chatbot created',
                'user_id': user_id,
                'chat': chatbot.__repr__(),
                'db': db_handler.__repr__()
            }
            return jsonify(to_return)
        else:
            return jsonify({'error': 'No data provided'})


@app.route('/api/get_history', methods=['GET'])
def send_favorites():
    global db_handler

    if request.method != 'GET':
        return jsonify({'error': 'Only GET requests are allowed'})
    else:
        if not db_handler:
            return jsonify({'error': 'Chatbot not created yet'})
        else:
            history = db_handler.get_history()
            return jsonify({'history': history})




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

