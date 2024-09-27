import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import datetime

r = sr.Recognizer()

def speak(command):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(command)
    engine.runAndWait()

def commands():
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)  # Corrected function spelling
            print('Listening... Ask Now...')
            audioin = r.listen(source)
            my_text = r.recognize_google(audioin)
            my_text = my_text.lower()
            print(my_text)
            
            # Play song
            if 'play' in my_text:
                my_text = my_text.replace('play', '')
                speak('Playing ' + my_text)
                pywhatkit.playonyt(my_text)
            
            # Ask date
            elif 'date' in my_text:
                today = datetime.date.today().strftime('%B %d, %Y')
                speak(f"Today's date is {today}")
            
            # Ask time
            elif 'time' in my_text:
                timenow = datetime.datetime.now().strftime('%I:%M %p')
                speak(f"The current time is {timenow}")
            
            # Ask about a person
            elif "who is" in my_text:
                person = my_text.replace('who is', '')
                info = wikipedia.summary(person, 1)
                print(info)
                speak(info)
                
            else:
                speak("Please ask a correct question.")
                
    except sr.UnknownValueError:
        print("Sorry, I did not understand the audio.")
        speak("Sorry, I did not understand that.")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        speak("I am having trouble connecting to the service.")
    except Exception as e:
        print(f"Error in the microphone: {e}")  # Detailed error message
        speak(f"There was an error: {e}")

while True:
    commands()
