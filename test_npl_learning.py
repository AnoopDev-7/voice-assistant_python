import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import datetime
import spacy
import time
import json

# Load the small English NLP model
nlp = spacy.load("en_core_web_sm")

# Initialize recognizer and text-to-speech engine
r = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Dictionary to store learned commands and their responses
learned_commands = {}

# Load previously learned commands from a file (if exists)
try:
    with open("learned_commands.json", "r") as file:
        learned_commands = json.load(file)
except FileNotFoundError:
    print("No learned commands file found, starting fresh.")

def speak(text):
    """
    Convert text to speech.
    """
    engine.say(text)
    engine.runAndWait()

def save_learned_commands():
    """
    Save learned commands to a file for persistence.
    """
    with open("learned_commands.json", "w") as file:
        json.dump(learned_commands, file)

def learn_command(command):
    """
    Learn a new command by asking the user for the appropriate response.
    """
    speak("I don't know how to respond to that. How should I respond?")
    print("Listening for a new response...")

    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            response = r.recognize_google(audio).lower()
            print(f"Learned response: {response}")

            # Save the command and response
            learned_commands[command] = response
            save_learned_commands()
            speak("Got it! I have learned this command.")
    except Exception as e:
        print(f"Error learning new command: {e}")
        speak("Sorry, I couldn't understand that response.")

def process_command(command):
    """
    Process known and learned commands.
    """
    if command in learned_commands:
        # If the command is learned, use the stored response
        speak(learned_commands[command])
    elif 'play' in command:
        song = command.replace('play', '').strip()
        speak(f'Playing {song}')
        pywhatkit.playonyt(song)
    elif 'date' in command:
        today = datetime.date.today().strftime('%B %d, %Y')
        speak(f"Today's date is {today}")
    elif 'time' in command:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        speak(f"The current time is {current_time}")
    elif 'who is' in command:
        person = command.replace('who is', '').strip()
        info = wikipedia.summary(person, 1)
        print(info)
        speak(info)
    else:
        # Learn the new command if it is not known
        learn_command(command)

def listen_for_command():
    """
    Listens for a command after detecting the trigger word "Alexa".
    """
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print('Listening... Say "Alexa" to activate...')
            audio = r.listen(source)
            command = r.recognize_google(audio).lower()
            print(f"Recognized input: {command}")

            # Check for the trigger word "alexa"
            if 'alexa' in command:
                speak("Yes, I'm listening.")
                time.sleep(0.5)  # Short pause before listening for command

                print("Waiting for your command...")
                audio = r.listen(source)
                command = r.recognize_google(audio).lower()
                print(f"Command after trigger: {command}")

                # Process the recognized command
                process_command(command)
            else:
                print("Waiting for the trigger word 'Alexa'.")
                
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        speak("I am having trouble connecting to the service.")
    except Exception as e:
        print(f"Error in the microphone: {e}")

# Continuous listening loop
while True:
    listen_for_command()
