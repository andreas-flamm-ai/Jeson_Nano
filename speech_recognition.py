import speech_recognition as sr

r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)

try:
    print("You said: " + r.recognize_google(audio))
except sr.UnknownValueError:
    print("Could not understand audio")



import speech_recognition as sr
import pyttsx3
import time

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# Speak function
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Listen for voice command
def listen_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source, timeout=5)
    try:
        command = r.recognize_google(audio).lower()
        print(f"Recognized: {command}")
        return command
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        speak("Speech service is unavailable.")
        return ""

# Robot actions
def walk_cycle():
    speak("Walking forward.")
    # Insert your servo gait code here
    time.sleep(2)

def kick_ball():
    speak("Kicking the ball.")
    # Insert your kick sequence here
    time.sleep(1)

# Main loop
def voice_control_loop():
    speak("Ready for commands.")
    while True:
        cmd = listen_command()
        if "walk" in cmd:
            walk_cycle()
        elif "kick" in cmd:
            kick_ball()
        elif "stop" in cmd or "exit" in cmd:
            speak("Stopping voice control.")
            break
        else:
            speak("Unknown command. Try saying walk or kick.")

voice_control_loop()