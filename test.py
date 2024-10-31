from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import GoogleGenerativeAI


api_key = "AIzaSyDrKmt50SJv-Wgm9vJeR-kkckPFqtBdKuM"

def init_conversation(memory):
    
    llm = GoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)
    return  ConversationChain( llm=llm, verbose=False, memory=memory )


def chatbot():
    while True:
        try:
            user_input = input("User:")
            if user_input == "bye":
                print("Thank you AI chatbot")
                break
            else:
                conversation = init_conversation(memory)
                memory = ConversationBufferMemory()
                model_response = conversation.predict(input = user_input)
                return f"AI chatbot: {model_response}"
        except Exception as e:
            print(f"Error: {e}")
