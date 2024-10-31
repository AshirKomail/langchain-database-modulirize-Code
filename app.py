from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import GoogleGenerativeAI

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import pickle

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chatbot.db"
db = SQLAlchemy(app)



class Chatbot_db(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    User_id = db.Column(db.Integer )
    conversation_id = db.Column(db.Integer)
    memory = db.Column(db.LargeBinary ,nullable = False )


api_key = "AIzaSyDrKmt50SJv-Wgm9vJeR-kkckPFqtBdKuM"

def init_conversation(memory):
    
    llm = GoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)
    return ConversationChain( llm=llm, verbose=False, memory=memory )



@app.route("/", methods=["POST"])

def chatbot():
    if request.method == "POST":
        try:
            User_id = request.json["User_id"]
            conversation_id = request.json["conversation_id"]
            prompt = request.json["Prompt"]

            User = Chatbot_db.query.filter_by(User_id = User_id).first()

            if User:        
                conn = Chatbot_db.query.filter_by(User_id = User_id ,conversation_id = conversation_id).first()
                if conn:
                    memory = pickle.loads(conn.memory)
                    conversation = init_conversation(memory)
                    model_response = conversation.predict(input = prompt)
                    conn.memory = pickle.dumps(conversation.memory)
                    db.session.commit()
                    return model_response  
                             
                else:
                    memory = ConversationBufferMemory()
                    conversation = init_conversation(memory)
                    model_response = conversation.predict(input = prompt)
                    dumps_memory = pickle.dumps(conversation.memory)
                    chat = Chatbot_db( User_id=User_id, conversation_id=conversation_id, memory = dumps_memory)

                    db.session.add(chat)
                    db.session.commit()
                    return model_response
            
            else:                    
                # print(f"New User created: {User_id}")
                print(f"New conversation created for User: {User_id} with conversation ID: {conversation_id}")
                
             
                memory=ConversationBufferMemory()
                conversation = init_conversation(memory)
                model_response = conversation.predict(input=prompt)
                memory_dumps = pickle.dumps(conversation.memory)

                chat = Chatbot_db(User_id = User_id , conversation_id=conversation_id, memory = memory_dumps)
                
                db.session.add(chat)                    
                db.session.commit()
                
                return model_response
        except Exception as e:
            return jsonify(f"Error: {e}")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
app.run(debug=True)