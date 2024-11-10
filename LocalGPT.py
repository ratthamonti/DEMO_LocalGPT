from os import system
import speech_recognition as sr
from gpt4all import GPT4All
import sys
import whisper
import warnings
import time
import pyautogui
import webbrowser
import os

#โหลดโมเดล GPT4
try:
    model = GPT4All("C:\\Users\\ninen\\Documents\\dev\\Python\\LocalGPT\\gpt4all-falcon-newbpe-q4_0.gguf", allow_download=False)
    print("Model loaded successfully!")
except Exception as e:
    print("Error loading model:", e)

assistant_name = "Roz"
listening_for_trigger_word = True
should_run = True
source = sr.Microphone()
recognizer = sr.Recognizer()

#กำหนดโมเดลสำหรับพูด
base_model_path = os.path.expanduser('~/.cache/whisper/base.pt')
base_model = whisper.load_model(base_model_path)

if sys.platform != 'darwin':
    import pyttsx3
    engine = pyttsx3.init()

tasks = []
listeningToTask = False
askingAQuestion = False

def respond(text):
    if sys.platform == 'darwin':
        ALLOWED_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,?!-_$:+-/ ")
        clean_text = ''.join(c for c in text if c in ALLOWED_CHARS)
        system(f"say '{clean_text}'")
    else:
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id) #กำหนดเสียงพูด ชาย หญิง
        engine.say(text)
        engine.runAndWait()

#ฟังก์ชั่นก์รอฟังคำสั่ง
def listen_for_command():
    with source as s:
        print("Listening for commands...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        with open("command.wav", "wb") as f:
            f.write(audio.get_wav_data())
        command = base_model.transcribe("command.wav")
        if command and command['text']:
            print("You said:", command['text'])
            return command['text'].lower()
        return None
    except sr.UnknownValueError:
        print("Could not understand audio. Please try again.")
        return None
    except sr.RequestError:
        print("Unable to access the Google Speech Recognition API.")
        return None

#หลังจากได้รับคำสั่งมาแล้วจะนำคำที่ได้ยินมาเปรียบเทียบกับคำสั่งที่มี
def perform_command(command):
    global tasks
    global listeningToTask
    global askingAQuestion
    global should_run
    global listening_for_trigger_word
    if command:
        print("Command: ", command)

        if "who is the most face of the vagina" in command:
            respond("Athirofski Pimzharkov")
            respond("and here the facebook")
            webbrowser.open("https://www.facebook.com/athirat.pimsaka.1")
            return
        
        if "who created you?" in command:
            respond("Ratthamonti Wasan He is my creator. He created me just because he wanted to create.")
            respond("and here the facebook")
            webbrowser.open("https://www.facebook.com/ninenoy.ya")
            return

        if listeningToTask:
            tasks.append(command)
            listeningToTask = False
            respond("Adding " + command + " to your task list. You have " + str(len(tasks)) + " currently in your list.")
        elif "add a task" in command:
            listeningToTask = True
            respond("Sure, what is the task?")
        elif "list tasks" in command:
            respond("Sure. Your tasks are:")
            for task in tasks:
                respond(task)
        elif "take a screenshot" in command:
            pyautogui.screenshot("screenshot.png")
            respond("I took a screenshot for you.")
        elif "open youtube" in command:
            respond("Opening Youtube.")
            webbrowser.open("https://youtu.be/QJCOmcU1JNY?si=Lm_1QbiiMTzEdV1E")
        elif "ask a question" in command:
            askingAQuestion = True
            respond("What's your question?")
            return
        elif askingAQuestion:
            askingAQuestion = False
            respond("Thinking...")
            print("User command: ", command)
            try:
                question = "Question: " + command
                output = model.generate(question, max_tokens=200)
                print("Model output: ", output)
                if output:
                    respond(output)
                else:
                    respond("Sorry, I couldn't generate a response.")
            except Exception as e:
                print("Error generating response:", e)
                respond("Sorry, I couldn't generate a response.")
        elif "exit" in command:
            should_run = False
        else:
            respond("Sorry, I'm not sure how to handle that command.")
    listening_for_trigger_word = True


def main():
    global listening_for_trigger_word
    while should_run:
        command = listen_for_command()
        if listening_for_trigger_word:
            listening_for_trigger_word = False
        else:
            perform_command(command)
        time.sleep(1)
    respond("Goodbye.")

if __name__ == "__main__":
    main()
