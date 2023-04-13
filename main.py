import speech_recognition as sr
import pyttsx3
import openai
import tkinter as tk

openai.api_key = "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"

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[1].id)

r = sr.Recognizer()
mic = sr.Microphone(device_index=1)

username = "ria"
botname = "bardem"


def start():
    status_label.config(text="Running...")
    start_listening()


def start_listening():
    conversation = ""
    while True:
        with mic as source:
            print('\n Listening...')
            r.adjust_for_ambient_noise(source, duration=0.2)
            audio = r.listen(source, phrase_time_limit=5)
        print('Processing...')

        try:
            user_input = r.recognize_google(audio)
        except:
            continue

        if user_input == "stop":
            print("Stopped")
            status_label.config(text="Stopped")
            break

        prompt = username + ":" + user_input + "\n" + botname + ":"
        conversation += prompt

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=conversation,
            temperature=0.83,
            max_tokens=279,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        response_str = response["choices"][0]["text"].replace("\n", "")
        response_str = response_str.split(
            username + ":", 1)[0].split(botname + ":", 1)[0]

        conversation += response_str + "\n"
        print(response_str)

        engine.say(response_str)
        engine.runAndWait()


# GUI

root = tk.Tk()
root.title("Voice Assistant")
root.geometry("300x200")

start_button = tk.Button(root, text="Start", command=start, height=3, width=10)
start_button.pack(pady=30)

status_label = tk.Label(root, text="Stopped")
status_label.pack()

instruction_label = tk.Label(root, text="Say 'stop' to stop")
instruction_label.pack(side=tk.BOTTOM, pady=10)

root.mainloop()
