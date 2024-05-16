import speech_recognition as sr
import streamlit as st
import cv2
import numpy as np
from PIL import Image
import PIL.Image
import google.generativeai as genai
import io
import pyttsx3

GOOGLE_API_KEY = "AIzaSyCFCTIrWmLiA3HRPIiT-USAdeiXXwyr4UQ"


def get_user_audio(duration=3):
    """
    Captures audio from the user's microphone and converts it to text.

    Parameters:
    duration (int): The duration in seconds for which the audio is recorded. Default is 5 seconds.

    Returns:
    str: The recognized text from the audio.
    """
    # Initialize recognizer class (for recognizing the speech)
    recognizer = sr.Recognizer()

    # Capture the audio from the default microphone
    with sr.Microphone() as source:
        print("Recording audio...")
        # Record the audio for the specified duration
        audio_data = recognizer.record(source, duration=duration)
        print("Recognizing...")

        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "Google Speech Recognition could not understand audio"
        except sr.RequestError as e:
            return f"Could not request results from Google Speech Recognition service; {e}"


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


def configure_genai():
    """Configures the Generative AI client with your API key."""
    if not GOOGLE_API_KEY:
        st.error(
            "Please set your Google Cloud project's Generative AI API key in a `.env` file.")
        return None

    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        return genai.GenerativeModel("gemini-pro-vision")
    except Exception as e:
        st.error(f"Error configuring Generative AI: {e}")
        return None


def capture_image():
    """Captures a frame from the webcam using OpenCV."""
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    return frame


def convert_cv2_to_pil(cv2_image):
    """Converts a OpenCV image to a PIL Image object."""
    rgb_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
    return PIL.Image.fromarray(rgb_image)


def get_image_description(image,prompt):
    """Retrieves an image description from the Generative AI client."""
    model = configure_genai()
    if not model:
        return None

    pil_image = convert_cv2_to_pil(image)
    try:
        
        response = model.generate_content(
            [prompt, pil_image], stream=True)
        # response = model.generate_content(["if their is a person recognise him or her, keep it short", pil_image], stream=True)
        response.resolve()
        return response.text
    except Exception as e:
        st.error(f"Error generating image description: {e}")
        return None


def main():
    """Main function to run the Streamlit app."""
    st.title(
        "AI Vision for Visually Imapaired \n Gaurish Ojha, Sanjeev Kushwaha, Shiva Chunbuk")

    has_camera = st.camera_input("Capture Image")

    if has_camera:
        # Convert the Streamlit UploadedFile object to a PIL Image
        image_pil = Image.open(io.BytesIO(has_camera.getvalue()))
        # Convert the PIL Image to a NumPy array for OpenCV processing
        image = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)


        st.image(image, channels="BGR")
        speak_text("Please ask your query")
        text = get_user_audio()
        print(text)
        if "stop" in text:
            speak_text("bye bye have a nice day meow ")
            return
        
        if "description" in text:
            prompt = "Explain the description in the image for a blind person, keep it short"
            description = get_image_description(image,prompt)
            if description:
                st.success(f"Image Description:\n{description}")
                speak_text(description)
            else:
                st.warning("Failed to generate image description.")
        elif "recognise" or "recognize" in text:
            prompt = "If you are able to recognize the person tell me about it, keep it short"
            description = get_image_description(image,prompt)
            if description:
                st.success(f"Image Description:\n{description}")
                speak_text(description)
            else:
                st.warning("Failed to generate image description.")
        elif "explain" or "extraction" or "text" in text:
            prompt = "extract the text and tell what is in it , keep it short"
            description = get_image_description(image,prompt)
            if description:
                st.success(f"Image Description:\n{description}")
                speak_text(description)
            else:
                st.warning("Failed to generate image description.")
        else:
            prompt  = f"""here is a instruction from a blind person,generate a necessary response based on "instruction",use the data in the image as well and keep it short, "instruction":{instruction} """
            description = get_image_description(image, prompt)
            if description:
                st.success(f"Image Description:\n{description}")
                speak_text(description)
            else:
                st.warning("Failed to generate image description.")
        

    

if __name__ == "__main__":
    main()
