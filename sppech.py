import pyttsx3
# Initialize the TTS engine
def speak_text(text):
    # Initialize the TTS engine
    speaker = pyttsx3.init()
    # Set properties: rate and volume
    speaker.setProperty('rate', 150)
    speaker.setProperty('volume', 1.0)
    # Speak the provided text
    speaker.say(text)
    # Block while processing all the currently queued commands
    speaker.runAndWait()
def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio).lower()
            print(f"You said: {text}")
            
            if "recognize" in text:
                speak_text("recognising")
            elif "read" in text:
                speak_text("reading")
            elif "description" in text:
                speak_text("describing")
            else:
                speak_text("I didn't understand the command.")
        except sr.UnknownValueError:
            speak_text("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            speak_text("Could not request results from the service; {0}".format(e))



if __name__ =="__main__":
    print(get_user_audio())