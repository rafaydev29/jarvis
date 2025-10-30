import pyttsx3
import speech_recognition as sr
import webbrowser
import pywhatkit
import wikipedia
import pyjokes
import datetime
import sys

def speak(text):
    """Speak the given text aloud"""
    print(f"Jarvis: {text}")
    engine = pyttsx3.init('sapi5')  
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  
    engine.setProperty('rate', 170)            
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def greet():
    """Greet the user based on the time"""
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning sir!")
    elif hour < 18:
        speak("Good afternoon sir!")
    else:
        speak("Good evening sir!")
    speak("Jarvis online and ready!")



def take_command():
    """Listen for the user's command and return it as text"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🎙️ Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 300
        try:
            audio = r.listen(source, timeout=6, phrase_time_limit=8)
        except sr.WaitTimeoutError:
            print("⏱️ Listening timed out.")
            return ""

    try:
        print("🧠 Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"✅ You said: {query}\n")
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn’t catch that. Could you please repeat?")
        return ""
    except sr.RequestError:
        speak("Network error. Please check your internet connection.")
        return ""
    except Exception as e:
        print(f"⚠️ Error: {e}")
        speak("Something went wrong while recognizing your voice.")
        return ""

def main():
    greet()
    while True:
        command = take_command()

        if command.strip() == "":
            continue

        speak(f"You said: {command}")


        if "time" in command:
            time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The time is {time}")

        elif "date" in command:
            date = datetime.datetime.now().strftime("%B %d, %Y")
            speak(f"Today's date is {date}")

        elif "open youtube" in command:
            speak("Opening YouTube now.")
            webbrowser.open("https://youtube.com")

        elif "open google" in command:
            speak("Opening Google now.")
            webbrowser.open("https://google.com")

        elif "play" in command:
            song = command.replace("play", "").strip()
            speak(f"Playing {song} on YouTube.")
            pywhatkit.playonyt(song)

        elif "wikipedia" in command:
            topic = command.replace("wikipedia", "").strip()
            speak(f"Searching Wikipedia for {topic}.")
            try:
                info = wikipedia.summary(topic, sentences=2)
                speak(info)
            except wikipedia.exceptions.DisambiguationError:
                speak("There are multiple results, please be more specific.")
            except wikipedia.exceptions.PageError:
                speak("Sorry, I couldn't find anything on Wikipedia for that topic.")

        elif "joke" in command:
            speak("Here's a joke for you.")
            joke = pyjokes.get_joke()
            speak(joke)

        elif any(word in command for word in ["exit", "quit", "stop", "close"]):
            speak("Goodbye sir, have a great day!")
            sys.exit()

        else:
            speak("Sorry, I didn't understand that. Please try again.")



if __name__ == "__main__":
    main()
