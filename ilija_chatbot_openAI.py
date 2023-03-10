import random
import os
import pickle
import openai

class Chatbot:
    def __init__(self):
        desktop_path = os.path.expanduser("~/Desktop")
        self.history_file = os.path.join(desktop_path, "chatbot_history.txt")
        self.responses_file = os.path.join(desktop_path, "chatbot_responses.pickle")
        self.responses = {}
        self.name = input("Hallo, wie ist dein Name? ")
        self.openai_key = "Hier bitte die OpenAI API-KEY eintragen"
        self.load_responses()

    def load_responses(self):
        try:
            with open(self.responses_file, "rb") as f:
                self.responses = pickle.load(f)
        except FileNotFoundError:
            self.responses = {}

    def save_responses(self):
        with open(self.responses_file, "wb") as f:
            pickle.dump(self.responses, f)

    def learn(self, input_text, response):
        self.responses[input_text] = response
        self.save_responses()

    def respond(self, input_text):
        if input_text in self.responses:
            return self.responses[input_text]
        elif input_text in ["Hallo", "Guten Tag", "Wer bist du ?", "Wer bist du?", "wer bist du?", "wer bist du ?", "Wie ist dein Name ?", "Wie ist dein Name?", "wie ist dein name?", "wie ist dein name ?"]:
            return "Hallo, meine Name ist Ilija, ich bin ein selbstlernender Chatbot. Was kann ich für dich tun ?"
        else:
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt="User: " + input_text,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.5,
                api_key=self.openai_key
            ).choices[0].text.strip()
            return response

    def chat(self):
        with open(self.history_file, "a") as f:
            while True:
                input_text = input(f"{self.name}: ")
                if input_text == "Tschüss":
                    break
                response = self.respond(input_text)
                if response == "Ich habe keine Antwort auf diese Frage.":
                    learn = input("Ilija: " + response + " Soll ich eine lernen? (Ja/Nein)")
                    if learn == "Ja":
                        response = input("Ilija: Was soll ich als Antwort lernen? ")
                        self.learn(input_text, response)
                    else:
                        self.learn(input_text, "Ich habe keine Antwort auf diese Frage, aber ich lerne gerne von dir.")
                print("Ilija: " + response)
                f.write(f"{self.name}: {input_text}\n")
                f.write(f"Ilija: {response}\n")
                self.learn(input_text, response)

    def print_history(self):
        with open(self.history_file, "r") as f:
            print(f.read())

chatbot = Chatbot()
print("Herzlich Willkommen! Der Chatbot wurde ordnungsgemäß gestartet und steht nun zur Unterhaltung bereit.")
print("Ilija nutzt OpenAI, um auf Fragen zu antworten, aber du kannst ihm auch beibringen, was es sagen soll.")
print("Ilija ist noch sehr jung und kennt daher noch nicht viele Begriffe.")
print("Du kannst Ilija aber alles beibringen, was es dir antworten soll.")
print("Um Ilija wieder zu verlassen, schreibe 'Tschüss'.")

chatbot.chat()

print("Dein Chatverlauf:")
chatbot.print_history()


