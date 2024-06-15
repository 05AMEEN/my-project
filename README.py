import speech_recognition as sr
import pyttsx3
import os
import openai

from dotenv import load_dotenv

load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_KEY')
openai.api_key = OPENAI_KEY

def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def record_text():
    recognizer = sr.Recognizer()
    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("Listening...")
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio)
                return text
        except sr.RequestError as e:
            print("Could not request result: {}".format(e))
        except sr.UnknownValueError:
            print("Unknown error occurred")

def send_to_chatGPT(messages):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=messages,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = response.choices[0].text.strip()
    return message

def main():
    messages = ""
    while True:
        user_input = record_text()
        messages += "User: " + user_input + "\n"
        response = send_to_chatGPT(messages)
        speak_text(response)
        messages += "AI: " + response + "\n"
        print("AI:", response)

if __name__ == "__main__":
    main()
